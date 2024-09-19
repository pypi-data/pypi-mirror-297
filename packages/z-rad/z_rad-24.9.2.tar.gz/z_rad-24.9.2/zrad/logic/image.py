import copy
import os
import warnings
from datetime import datetime

import SimpleITK as sitk
import numpy as np
import pydicom
from pydicom.errors import InvalidDicomError
from skimage import draw

from zrad.logic.exceptions import DataStructureWarning, DataStructureError


def parse_time(time_str):
    """
    Parse a time string into a datetime object using various possible formats.

    Args:
        time_str (str): The time string to parse.

    Returns:
        datetime: Parsed datetime object.

    Raises:
        ValueError: If the time string does not match any expected formats.
    """
    for fmt in ('%H%M%S.%f', '%H%M%S', '%Y%m%d%H%M%S.%f'):
        try:
            return datetime.strptime(time_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"time data '{time_str}' does not match expected formats")


class Image:
    def __init__(self, array=None, origin=None, spacing=None, direction=None, shape=None):
        self.sitk_image = None
        self.array = array
        self.origin = origin
        self.spacing = spacing
        self.direction = direction
        self.shape = shape

    def copy(self):
        return Image(
            array=copy.deepcopy(self.array),
            origin=copy.deepcopy(self.origin),
            spacing=copy.deepcopy(self.spacing),
            direction=copy.deepcopy(self.direction),
            shape=copy.deepcopy(self.shape)
        )

    def save_as_nifti(self, output_path):
        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))
        img = sitk.GetImageFromArray(self.array)
        img.SetOrigin(self.origin)
        img.SetSpacing(self.spacing)
        img.SetDirection(self.direction)
        sitk.WriteImage(img, output_path)

    def read_nifti_image(self, image_path):
        sitk_reader = sitk.ImageFileReader()
        sitk_reader.SetImageIO("NiftiImageIO")
        sitk_reader.SetFileName(image_path)
        image = sitk_reader.Execute()
        array = sitk.GetArrayFromImage(image)
        self.sitk_image = image
        self.array = array.astype(np.float64)
        self.origin = image.GetOrigin()
        self.spacing = np.array(image.GetSpacing())
        self.direction = image.GetDirection()
        self.shape = image.GetSize()

    def read_nifti_mask(self, image, mask_path):
        sitk_reader = sitk.ImageFileReader()
        sitk_reader.SetImageIO("NiftiImageIO")
        sitk_reader.SetFileName(mask_path)
        mask = sitk_reader.Execute()
        array = sitk.GetArrayFromImage(mask)
        self.sitk_image = image
        self.array = array.astype(np.float64)
        self.origin = image.origin
        self.spacing = image.spacing
        self.direction = image.direction
        self.shape = image.shape

    def read_dicom_image(self, dicom_dir, modality):
        dicom_files = get_dicom_files(directory=dicom_dir, modality=modality)
        validate_z_spacing(dicom_files)
        image = process_dicom_series(dicom_dir, dicom_files)
        if modality == 'PET':
            validate_pet_dicom_tags(dicom_files)
            image = apply_suv_correction(dicom_files, image)
        if image:
            array = sitk.GetArrayFromImage(image)
            self.sitk_image = image
            self.array = array.astype(np.float64)
            self.origin = image.GetOrigin()
            self.spacing = np.array(image.GetSpacing())
            self.direction = image.GetDirection()
            self.shape = image.GetSize()

    def read_dicom_mask(self, dicom_dir, structure_name, image):
        dicom_files = get_dicom_files(directory=dicom_dir, modality='RTSTRUCT')
        if len(dicom_files) != 1:
            msg = f"Expected one RTSTRUCT file but found {len(dicom_files)}"
            raise DataStructureError(msg)

        mask = extract_dicom_mask(dicom_files[0], structure_name, image.sitk_image)
        self.array = mask.array
        self.origin = mask.origin
        self.spacing = mask.spacing
        self.direction = mask.direction
        self.shape = mask.shape


def get_dicom_files(directory, modality):
    """
    Recursively scans a directory and its subdirectories for DICOM files with the specified modality.

    Args:
        directory (str): The path to the directory containing files to be checked.

    Returns:
        list: A list of file paths for valid DICOM files with the specified modality.
    """
    modality_mapping = {'PET': 'PT', 'CT': 'CT', 'MRI': 'MR', 'RTSTRUCT': 'RTSTRUCT'}
    modality_dicom = modality_mapping[modality]

    dicom_files = []  # List to store valid DICOM files with the specified modality

    # Walk through all directories and subdirectories
    for root, _, files in os.walk(directory):
        for f in files:
            file_path = os.path.join(root, f)  # Full path of the file

            try:
                # Try to read the DICOM file without loading pixel data
                dcm = pydicom.dcmread(file_path, stop_before_pixels=True)

                # Check if the DICOM file's Modality matches the desired modality
                if dcm.Modality == modality_dicom:
                    dicom_files.append(file_path)  # Add to the list if Modality matches

            except InvalidDicomError:
                # File is not a valid DICOM; skip it
                continue
            except Exception as e:
                # Handle any other unexpected exceptions
                warning_msg = f"An error occurred while processing file {file_path}: {str(e)}"
                warnings.warn(warning_msg, DataStructureWarning)
    return dicom_files


def validate_z_spacing(dicom_files):
    slice_z_origin = []
    for dcm_file in dicom_files:
        dicom_file_path = dcm_file
        dicom = pydicom.dcmread(dicom_file_path)
        slice_z_origin.append(float(dicom.ImagePositionPatient[2]))
    slice_z_origin = sorted(slice_z_origin)
    slice_thickness = [abs(slice_z_origin[i] - slice_z_origin[i + 1]) for i in range(len(slice_z_origin) - 1)]
    for i in range(len(slice_thickness) - 1):
        if abs((slice_thickness[i] - slice_thickness[i + 1])) > 10 ** (-3):
            error_msg = f'Inconsistent z-spacing. Absolute deviation is more than 0.001 mm.'
            raise DataStructureError(error_msg)


def validate_pet_dicom_tags(dicom_files):
    time_mismatch = False
    acquisition_time_list = []
    for dcm_file in dicom_files:
        dicom_file_path = dcm_file
        dicom = pydicom.dcmread(dicom_file_path)
        acquisition_time_list.append(parse_time(dicom.AcquisitionTime))

        dicom_file_path = dcm_file
        dicom = pydicom.dcmread(dicom_file_path)
        image_id = dicom_file_path

        try:
            pat_weight = dicom[(0x0010, 0x1030)].value
            if float(pat_weight) < 1:
                warning_msg = f"For patient's {image_id} image, patient's weight tag (0071, 1022) contains weight < 1kg. Patient is excluded from the analysis."
                warnings.warn(warning_msg, DataStructureWarning)

        except KeyError:
            warning_msg = f"For patient's {image_id} image, patient's weight tag (0071, 1022) is not present. Patient is excluded from the analysis."
            warnings.warn(warning_msg, DataStructureWarning)
        if 'DECY' not in dicom[(0x0028, 0x0051)].value or 'ATTN' not in dicom[(0x0028, 0x0051)].value:
            warning_msg = f"For patient's {image_id} image, in DICOM tag (0028, 0051) either no 'DECY' (decay correction) or 'ATTN' (attenuation correction). Patient is excluded from the analysis."
            warnings.warn(warning_msg, DataStructureWarning)

        if dicom.Units == 'BQML':
            injection_time = parse_time(
                dicom.RadiopharmaceuticalInformationSequence[0].RadiopharmaceuticalStartTime)
            if dicom.DecayCorrection == 'START':
                if 'PHILIPS' in dicom.Manufacturer.upper():
                    acquisition_time = np.min(acquisition_time_list)
                elif 'SIEMENS' in dicom.Manufacturer.upper():
                    try:
                        acquisition_time = parse_time(dicom[(0x0071, 0x1022)].value).replace(
                            year=injection_time.year,
                            month=injection_time.month,
                            day=injection_time.day)
                        if (acquisition_time != np.min(acquisition_time_list)
                                or acquisition_time != parse_time(dicom.SeriesTime) and not time_mismatch):
                            time_mismatch = True
                            warning_msg = f"For patient's {image_id} image, there is a mismatch between the earliest acquisition time, series time and Siemens private tag (0071, 1022). Time from the Siemens private tag was used."
                            warnings.warn(warning_msg, DataStructureWarning)
                    except KeyError:
                        acquisition_time = np.min(acquisition_time_list)
                        if not time_mismatch:
                            time_mismatch = True
                            warning_msg = f"For patient's {image_id} image, private Siemens tag (0071, 1022) is not present. The earliest of all acquisition times was used."
                            warnings.warn(warning_msg, DataStructureWarning)

                        if acquisition_time != parse_time(dicom.SeriesTime) and not time_mismatch:
                            time_mismatch = True
                            warning_msg = f"For patient's {image_id} image, a mismatch present between the earliest acquisition time and series time. Earliest acquisition time was used."
                            warnings.warn(warning_msg, DataStructureWarning)
                elif 'GE' in dicom.Manufacturer.upper():
                    try:
                        acquisition_time = parse_time(dicom[(0x0009, 0x100d)].value).replace(
                            year=injection_time.year,
                            month=injection_time.month,
                            day=injection_time.day)
                        if (acquisition_time != np.min(acquisition_time_list)
                                or acquisition_time != parse_time(dicom.SeriesTime) and not time_mismatch):
                            time_mismatch = True
                            warning_msg = f"For patient's {image_id} image, a mismatch present between the earliest acquisition time, series time, and GE private tag. Time from the GE private tag was used."
                            warnings.warn(warning_msg, DataStructureWarning)
                    except KeyError:
                        acquisition_time = np.min(acquisition_time_list)
                        if not time_mismatch:
                            time_mismatch = True
                            warning_msg = f"For patient's {image_id} image, private GE tag (0009, 100d) is not present. The earliest of all acquisition times was used."
                            warnings.warn(warning_msg, DataStructureWarning)
                        if acquisition_time != parse_time(dicom.SeriesTime) and not time_mismatch:
                            time_mismatch = True
                            warning_msg = f"For patient's {image_id} image, a mismatch present between the earliest acquisition time and series time. Earliest acquisition time was used."
                            warnings.warn(warning_msg, DataStructureWarning)
                else:
                    warning_msg = f"For patient's {image_id} image, an unknown PET scaner manufacturer is present. Z-Rad only supports Philips, Siemens, and GE."
                    raise DataStructureError(warning_msg)

            elif dicom.DecayCorrection == 'ADMIN':
                acquisition_time = injection_time

            else:
                warning_msg = f"For patient's {image_id} image, An unsupported Decay Correction {dicom.DecayCorrection} is present. Only supported are 'START' and 'ADMIN'. Patient is excluded from the analysis."
                raise DataStructureError(warning_msg)
            elapsed_time = (acquisition_time - injection_time).total_seconds()
            if elapsed_time < 0:
                error_msg = f"For patient's {image_id} image, patient is excluded from the analysis due to the negative time difference in the decay factor."
                raise DataStructureError(error_msg)
            elif elapsed_time > 0 and abs(elapsed_time) < 1800 and dicom.DecayCorrection != 'ADMIN':
                warning_msg = f"Only {abs(elapsed_time) / 60} minutes after the injection."
                warnings.warn(warning_msg, DataStructureWarning)
        elif dicom.Units == 'CNTS' and 'PHILIPS' in dicom.Manufacturer.upper():
            try:
                activity_scale_factor = dicom[(0x7053, 0x1009)].value
                print(activity_scale_factor)
                if activity_scale_factor == 0.0:
                    error_msg = f"For patient's {image_id} image, patient is excluded, Philips private activity scale factor (7053, 1009) = 0. (PET units CNTS)"
                    raise DataStructureError(error_msg)
            except KeyError:
                error_msg = f"For patient's {image_id} image, patient is excluded, Philips private activity scale factor (7053, 1009) is missing. (PET units CNTS)."
                raise DataStructureError(error_msg)
        else:
            error_msg = f"For patient's {image_id} image, patient is excluded, only supported PET Units are BQML for Philips, Siemens and GE or CNTS for Philips"
            raise DataStructureError(error_msg)


def apply_suv_correction(dicom_files, suv_image):
    def calculate_suv(dicom_file_path, min_acquisition_time):

        ds = pydicom.dcmread(dicom_file_path)
        units = ds.Units
        injection_time = parse_time(ds.RadiopharmaceuticalInformationSequence[0].RadiopharmaceuticalStartTime)

        if ds.DecayCorrection == 'START':
            if 'PHILIPS' in ds.Manufacturer.upper():
                acquisition_time = min_acquisition_time
            elif 'SIEMENS' in ds.Manufacturer.upper() and units == 'BQML':
                try:
                    acquisition_time = parse_time(ds[(0x0071, 0x1022)].value).replace(year=injection_time.year,
                                                                                      month=injection_time.month,
                                                                                      day=injection_time.day)
                except KeyError:
                    acquisition_time = min_acquisition_time
            elif 'GE' in ds.Manufacturer.upper() and units == 'BQML':
                try:
                    acquisition_time = parse_time(ds[(0x0009, 0x100d)].value).replace(year=injection_time.year,
                                                                                      month=injection_time.month,
                                                                                      day=injection_time.day)
                except KeyError:
                    acquisition_time = min_acquisition_time
        elif ds.DecayCorrection == 'ADMIN':
            acquisition_time = injection_time

        patient_weight = float(ds.PatientWeight)
        injected_dose = float(ds.RadiopharmaceuticalInformationSequence[0].RadionuclideTotalDose)

        elapsed_time = (acquisition_time - injection_time).total_seconds()

        half_life = float(ds.RadiopharmaceuticalInformationSequence[0].RadionuclideHalfLife)
        decay_factor = np.exp(-1 * ((np.log(2) * elapsed_time) / half_life))

        decay_corrected_dose = injected_dose * decay_factor

        image_data = ds.pixel_array
        activity_concentration = (image_data * ds.RescaleSlope) + ds.RescaleIntercept

        if 'PHILIPS' in ds.Manufacturer.upper() and units == 'CNTS':
            activity_concentration = activity_concentration * ds[(0x7053, 0x1009)].value

        suv = activity_concentration / (decay_corrected_dose / (patient_weight * 1000))

        suv = suv.T

        return suv
    intensity_array = np.zeros(suv_image.GetSize())
    acquisition_time_list = []
    for dicom_file in dicom_files:
        dcm_data = pydicom.dcmread(dicom_file)
        acquisition_time_list.append(parse_time(dcm_data.AcquisitionTime))
    min_acquisition_time = np.min(acquisition_time_list)

    dicom_files = sorted(dicom_files, key=lambda f: float(pydicom.dcmread(f).ImagePositionPatient[2]))
    for z_slice_id, dicom_file in enumerate(dicom_files):
        intensity_array[:, :, z_slice_id] = calculate_suv(dicom_file, min_acquisition_time)

    # Flip from head to toe
    intensity_image = sitk.GetImageFromArray(intensity_array.T)
    intensity_image.SetOrigin(suv_image.GetOrigin())
    intensity_image.SetSpacing(np.array(suv_image.GetSpacing()))
    intensity_image.SetDirection(np.array(suv_image.GetDirection()))
    return intensity_image


def process_dicom_series(directory, dicom_files):
    reader = sitk.ImageSeriesReader()
    series_ids = reader.GetGDCMSeriesIDs(directory)
    if not series_ids:
        raise ValueError("No DICOM series found in the directory.")
    file_names = reader.GetGDCMSeriesFileNames(directory, series_ids[0])
    reader.SetFileNames(file_names)
    image = reader.Execute()

    slice_z_origin = []

    for dicom_file_path in dicom_files:
        dicom = pydicom.dcmread(dicom_file_path)
        if dicom.Modality in ['CT', 'PT', 'MR']:
            pixel_spacing = dicom.PixelSpacing
            slice_z_origin.append(float(dicom.ImagePositionPatient[2]))

    slice_z_origin = sorted(slice_z_origin)
    slice_thickness = abs(np.median([slice_z_origin[i] - slice_z_origin[i + 1]
                                     for i in range(len(slice_z_origin) - 1)]))

    image.SetSpacing((float(pixel_spacing[0]), float(pixel_spacing[1]), float(slice_thickness)))

    return image


def extract_dicom_mask(rtstruct_path, roi_name, image):

    def generate_mask_array(contours, dcm_im):
        dimensions = dcm_im.GetSize()

        # Create an empty mask with the same size and metadata as dcm_im
        mask_array = np.zeros(dcm_im.GetSize()[::-1], dtype=np.uint8)

        for contour in contours:
            if contour['type'].upper().replace('_', '').strip() not in ['CLOSEDPLANAR', 'INTERPOLATEDPLANAR',
                                                                        'CLOSEDPLANARXOR']:
                continue

            points = contour['points']
            transformed_points = np.array(
                [dcm_im.TransformPhysicalPointToContinuousIndex((points['x'][i], points['y'][i], points['z'][i]))
                 for i in range(len(points['x']))])

            z_coord = int(round(transformed_points[0, 2]))
            mask_layer = draw.polygon2mask([dimensions[0], dimensions[1]][::-1],
                                           np.column_stack((transformed_points[:, 1], transformed_points[:, 0])))
            updated_mask = np.logical_xor(mask_array[z_coord, :, :], mask_layer)
            mask_array[z_coord, :, :] = np.where(updated_mask, 1, 0)

        return mask_array

    def get_contour_data(file_path, selected_roi):
        def get_contour_coord(metadata, current_roi_sequence, skip_contours_bool=False):
            contour_info = {
                'name': getattr(metadata[current_roi_sequence.ReferencedROINumber], 'ROIName', 'unknown'),
                'roi_number': current_roi_sequence.ReferencedROINumber,
                'referenced_frame': getattr(metadata[current_roi_sequence.ReferencedROINumber],
                                            'ReferencedFrameOfReferenceUID', 'unknown'),
                'display_color': getattr(current_roi_sequence, 'ROIDisplayColor', [])
            }

            if not skip_contours_bool and hasattr(current_roi_sequence, 'ContourSequence'):
                contour_info['sequence'] = [{
                    'type': getattr(contour, 'ContourGeometricType', 'unknown'),
                    'points': {
                        'x': [contour.ContourData[i] for i in range(0, len(contour.ContourData), 3)],
                        'y': [contour.ContourData[i + 1] for i in range(0, len(contour.ContourData), 3)],
                        'z': [contour.ContourData[i + 2] for i in range(0, len(contour.ContourData), 3)]
                    }
                } for contour in current_roi_sequence.ContourSequence]

            return contour_info

        dicom_data = pydicom.dcmread(file_path)
        if not hasattr(dicom_data, 'StructureSetROISequence'):
            raise InvalidDicomError()

        contour_data = None
        metadata_map = {data.ROINumber: data for data in dicom_data.StructureSetROISequence}
        for roi_sequence in dicom_data.ROIContourSequence:
            roi_name = getattr(metadata_map[roi_sequence.ReferencedROINumber], 'ROIName', 'unknown')
            if roi_name == selected_roi:
                contour_data = get_contour_coord(metadata_map, roi_sequence)
                break

        return contour_data

    rt_struct = get_contour_data(rtstruct_path, roi_name)
    if rt_struct:
        mask = generate_mask_array(rt_struct['sequence'], image)
        return Image(array=mask,
                     origin=image.GetOrigin(),
                     spacing=np.array(image.GetSpacing()),
                     direction=image.GetDirection(),
                     shape=image.GetSize())
    else:
        return Image()


def get_all_structure_names(rtstruct_path):
    """Extracts all structure names from an RTSTRUCT DICOM file.

    Args:
        rtstruct_path (str): Path to the RTSTRUCT DICOM file.

    Returns:
        list: A list of structure names.

    Raises:
        InvalidDicomError: If the DICOM file does not have a StructureSetROISequence attribute.
    """
    # Read the DICOM file
    dicom_data = pydicom.dcmread(rtstruct_path)

    # Check if the file contains a StructureSetROISequence
    if not hasattr(dicom_data, 'StructureSetROISequence'):
        raise InvalidDicomError(f"The DICOM file at {rtstruct_path} is not a valid RTSTRUCT file.")

    # Map ROI numbers to metadata for quick lookup
    metadata_map = {roi_data.ROINumber: roi_data for roi_data in dicom_data.StructureSetROISequence}

    # Extract structure names
    structure_names = []
    if hasattr(dicom_data, 'ROIContourSequence'):
        for roi_sequence in dicom_data.ROIContourSequence:
            roi_number = roi_sequence.ReferencedROINumber
            roi_name = getattr(metadata_map.get(roi_number, {}), 'ROIName', 'unknown')
            structure_names.append(roi_name)

    return structure_names
