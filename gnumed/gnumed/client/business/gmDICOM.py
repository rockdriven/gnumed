# -*- coding: utf-8 -*-
#============================================================

from __future__ import print_function

__doc__ = """GNUmed DICOM handling middleware"""

__license__ = "GPL v2 or later"
__author__ = "K.Hilbert <Karsten.Hilbert@gmx.net>"


# stdlib
import io
import os
import sys
import logging
import httplib			# needed for exception names thrown by httplib2, duh |-(
import socket			# needed for exception names thrown by httplib2, duh |-(
import httplib2
import json
import zipfile
import shutil
from urllib import urlencode
import distutils.version as version


# GNUmed modules
if __name__ == '__main__':
	sys.path.insert(0, '../../')
from Gnumed.pycommon import gmTools
from Gnumed.pycommon import gmShellAPI
#from Gnumed.pycommon import gmPG2
#from Gnumed.pycommon import gmBusinessDBObject
#from Gnumed.pycommon import gmHooks
#from Gnumed.pycommon import gmDispatcher

_log = logging.getLogger('gm.dicom')

_map_gender_gm2dcm = {
	'm': 'M',
	'f': 'F',
	'tm': 'M',
	'tf': 'F',
	'h': None
}

#============================================================
class cOrthancServer:
	# REST API access to Orthanc DICOM servers

#	def __init__(self):
#		self.__server_identification = None
#		self.__user = None
#		self.__password = None
#		self.__conn = None
#		self.__server_url = None

	#--------------------------------------------------------
	def connect(self, host, port, user, password, expected_minimal_version=None, expected_name=None, expected_aet=None):
		if (host is None) or (host.strip() == u''):
			host = u'localhost'
		self.__server_url = u'http://%s:%s' % (host, port)
		self.__user = user
		self.__password = password
		_log.info('connecting as [%s] to Orthanc server at [%s]', self.__user, self.__server_url)
		self.__conn = httplib2.Http()
		self.__conn.add_credentials(self.__user, self.__password)
		_log.debug('connected to server: %s', self.server_identification)
		self.connect_error = u''
		if self.server_identification is False:
			self.connect_error += u'retrieving server identification failed'
			return False
		if expected_minimal_version is not None:
			if version.LooseVersion(self.server_identification['Version']) < version.LooseVersion(expected_min_version):
				_log.error('server too old, needed [%s]', expected_min_version)
				self.connect_error += u'server too old, needed version [%s]' % expected_min_version
				return False
		if expected_name is not None:
			if self.server_identification['Name'] != expected_name:
				_log.error('wrong server name, expected [%s]', expected_name)
				self.connect_error += u'wrong server name, expected [%s]' % expected_name
				return False
		if expected_aet is not None:
			if self.server_identification['DicomAet'] != expected_name:
				_log.error('wrong server AET, expected [%s]', expected_aet)
				self.connect_error += u'wrong server AET, expected [%s]' % expected_aet
				return False
		return True

	#--------------------------------------------------------
	def _get_server_identification(self):
		try:
			return self.__server_identification
		except AttributeError:
			pass
		system_data = self.__run_GET(url = '%s/system' % self.__server_url)
		if system_data is False:
			_log.error('unable to get server identification')
			return False
		_log.debug('server: %s', system_data)
		self.__server_identification = system_data
		return self.__server_identification

	server_identification = property(_get_server_identification, lambda x:x)

	#--------------------------------------------------------
	def _get_as_external_id_issuer(self):
		# fixed type :: user level instance name :: DICOM AET
		return u'Orthanc::%(Name)s::%(DicomAet)s' % self.__server_identification

	as_external_id_issuer = property(_get_as_external_id_issuer, lambda x:x)

	#--------------------------------------------------------
	def _get_url_browse_patients(self):
		if self.__user is None:
			return self.__server_url
		return self.__server_url.replace(u'http://', u'http://%s@' % self.__user)

	url_browse_patients = property(_get_url_browse_patients, lambda x:x)

	#--------------------------------------------------------
	def get_url_browse_patient(self, patient_id):
		# http://localhost:8042/#patient?uuid=0da01e38-cf792452-65c1e6af-b77faf5a-b637a05b
		return u'%s/#patient?uuid=%s' % (self.url_browse_patients, patient_id)

	#--------------------------------------------------------
	def get_url_browse_study(self, study_id):
		# http://localhost:8042/#study?uuid=0da01e38-cf792452-65c1e6af-b77faf5a-b637a05b
		return u'%s/#study?uuid=%s' % (self.url_browse_patients, study_id)

	#--------------------------------------------------------
	# download API
	#--------------------------------------------------------
	def get_matching_patients(self, person):
		_log.info(u'searching for Orthanc patients matching %s', person)

		# look for patient by external ID first
		pacs_ids = person.get_external_ids(id_type = u'PACS', issuer = self.as_external_id_issuer)
		if len(pacs_ids) > 1:
			_log.error('GNUmed patient has more than one ID for this PACS: %s', pacs_ids)
			_log.error('the PACS ID is expected to be unique per PACS')
			return []

		if len(pacs_ids) == 1:
			pats = self.get_patients_by_external_id(external_id = pacs_ids[0]['value'])
			if len(pats) > 1:
				_log.warning('more than one Orthanc patient matches PACS ID: %s', pacs_ids[0])
			if len(pats) > 0:
				return pats
			_log.debug('no external patient matches PACS ID: %s', pacs_ids[0])
			# return find type ? especially useful for non-matches on ID

		elif len(pacs_ids) == 0:
			_log.info('no PACS ID known for this patient')
			# search by name

#		# then look for name parts
#		name = person.get_active_name()
		return []

	#--------------------------------------------------------
	def get_patients_by_external_id(self, external_id=None):
		matching_patients = []
		_log.info(u'searching for patients with external ID >>>%s<<<', external_id)

		# elegant server-side approach:
		search_data = {
			'Level': 'Patient',
			'CaseSensitive': False,
			'Expand': True,
			'Query': {'PatientID': external_id.strip(u'*')}
		}
		_log.info(u'server-side C-FIND SCU over REST search, mogrified search data: %s', search_data)
		matches = self.__run_POST(url = u'%s/tools/find' % self.__server_url, data = search_data)

		# paranoia
		for match in matches:
			self.protect_patient(orthanc_id = match['ID'])
		return matches

#		# recursive brute force approach:
#		for pat_id in self.__run_GET(url = '%s/patients' % self.__server_url):
#			orthanc_pat = self.__run_GET(url = '%s/patients/%s' % (self.__server_url, pat_id))
#			orthanc_external_id = orthanc_pat['MainDicomTags']['PatientID']
#			if orthanc_external_id != external_id:
#				continue
#			_log.debug(u'match: %s (name=[%s], orthanc_id=[%s])', orthanc_external_id, orthanc_pat['MainDicomTags']['PatientName'], orthanc_pat['ID'])
#			matching_patients.append(orthanc_pat)
#		if len(matching_patients) == 0:
#			_log.debug(u'no matches')
#		return matching_patients

	#--------------------------------------------------------
	def get_patients_by_name(self, name_parts=None, gender=None, dob=None, fuzzy=False):
		_log.info(u'name parts %s, gender [%s], dob [%s], fuzzy: %s', name_parts, gender, dob, fuzzy)
		if len(name_parts) > 1:
			return self.get_patients_by_name_parts(name_parts = name_parts, gender = gender, dob = dob, fuzzy = fuzzy)
		if not fuzzy:
			search_term = name_parts[0].strip(u'*')
		else:
			search_term = name_parts[0]
			if not search_term.endswith(u'*'):
				search_term += u'*'
		search_data = {
			'Level': 'Patient',
			'CaseSensitive': False,
			'Expand': True,
			'Query': {'PatientName': search_term}
		}
		if gender is not None:
			gender = _map_gender_gm2dcm[gender.lower()]
			if gender is not None:
				search_data['Query']['PatientSex'] = gender
		if dob is not None:
			search_data['Query']['PatientBirthDate'] = dob.strftime('%Y%m%d')
		_log.info(u'server-side C-FIND SCU over REST search, mogrified search data: %s', search_data)
		matches = self.__run_POST(url = u'%s/tools/find' % self.__server_url, data = search_data)
		return matches

	#--------------------------------------------------------
	def get_patients_by_name_parts(self, name_parts=None, gender=None, dob=None, fuzzy=False):
		# fuzzy: allow partial/substring matches (but not across name part boundaries ',' or '^')
		matching_patients = []
		clean_parts = []
		for part in name_parts:
			if part.strip() == u'':
				continue
			clean_parts.append(part.lower().strip())
		_log.info(u'client-side patient search, scrubbed search terms: %s', clean_parts)
		pat_ids = self.__run_GET(url = '%s/patients' % self.__server_url)
		if pat_ids is False:
			_log.error(u'cannot retrieve patients')
			return []
		for pat_id in pat_ids:
			orthanc_pat = self.__run_GET(url = '%s/patients/%s' % (self.__server_url, pat_id))
			if orthanc_pat is False:
				_log.error('cannot retrieve patient')
				continue
			orthanc_name = orthanc_pat['MainDicomTags']['PatientName'].lower().strip()
			if not fuzzy:
				orthanc_name = orthanc_name.replace(u' ', u',').replace(u'^', u',').split(u',')
			parts_in_orthanc_name = 0
			for part in clean_parts:
				if part in orthanc_name:
					parts_in_orthanc_name += 1
			if parts_in_orthanc_name == len(clean_parts):
				_log.debug(u'name match: "%s" contains all of %s', orthanc_name, clean_parts)
				if gender is not None:
					gender = _map_gender_gm2dcm[gender.lower()]
					if gender is not None:
						if orthanc_pat['MainDicomTags']['PatientSex'].lower() != gender:
							_log.debug(u'gender mismatch: dicom=[%s] gnumed=[%s], skipping', orthanc_pat['MainDicomTags']['PatientSex'], gender)
							continue
				if dob is not None:
					if orthanc_pat['MainDicomTags']['PatientBirthDate'] != dob.strftime('%Y%m%d'):
						_log.debug(u'dob mismatch: dicom=[%s] gnumed=[%s], skipping', orthanc_pat['MainDicomTags']['PatientBirthDate'], dob)
						continue
				matching_patients.append(orthanc_pat)
			else:
				_log.debug(u'name mismatch: "%s" does not contain all of %s', orthanc_name, clean_parts)
		return matching_patients

	#--------------------------------------------------------
	def get_studies_list_by_patient_name(self, name_parts=None, gender=None, dob=None, fuzzy=False):
		return self.get_studies_list_by_orthanc_patient_list (
			orthanc_patients = self.get_patients_by_name(name_parts = name_parts, gender = gender, dob = dob, fuzzy = fuzzy)
		)

	#--------------------------------------------------------
	def get_studies_list_by_external_id(self, external_id=None):
		return self.get_studies_list_by_orthanc_patient_list (
			orthanc_patients = self.get_patients_by_external_id(external_id = external_id)
		)

	#--------------------------------------------------------
	def get_study_as_zip(self, study_id=None, filename=None):
		if filename is None:
			filename = gmTools.get_unique_filename(prefix = r'DCM-', suffix = r'.zip')
		_log.info('exporting study [%s] into [%s]', study_id, filename)
		f = io.open(filename, 'wb')
		f.write(self.__run_GET(url = '%s/studies/%s/archive' % (self.__server_url, study_id)))
		f.close()
		return filename

	#--------------------------------------------------------
	def get_study_as_zip_with_dicomdir(self, study_id=None, filename=None):
		if filename is None:
			filename = gmTools.get_unique_filename(prefix = r'DCM-', suffix = r'.zip')
		_log.info('exporting study [%s] into [%s]', study_id, filename)
		f = io.open(filename, 'wb')
		f.write(self.__run_GET(url = '%s/studies/%s/media' % (self.__server_url, study_id)))
		f.close()
		return filename

	#--------------------------------------------------------
	def get_studies_as_zip(self, study_ids=None, patient_id=None, filename=None):
		if filename is None:
			filename = gmTools.get_unique_filename(prefix = r'DCM-', suffix = r'.zip')
		if study_ids is None:
			_log.info('exporting all studies of patient [%s] into [%s]', patient_id, filename)
			f = io.open(filename, 'wb')
			f.write(self.__run_GET(url = '%s/patients/%s/archive' % (self.__server_url, patient_id)))
			f.close()
			return filename

	#--------------------------------------------------------
	def get_studies_as_zip_with_dicomdir(self, study_ids=None, patient_id=None, filename=None):
		if filename is None:
			filename = gmTools.get_unique_filename(prefix = r'DCM-', suffix = r'.zip')

		if study_ids is None:
			_log.info(u'exporting all studies of patient [%s] into [%s]', patient_id, filename)
			f = io.open(filename, 'wb')
			url = '%s/patients/%s/media' % (self.__server_url, patient_id)
			_log.debug(url)
			f.write(self.__run_GET(url = url))
			f.close()
			return filename

#		return u'get range of studies as zip with dicomdir not implemented, either all or one'

		dicomdir_cmd = u'gm-create_dicomdir'		# args: 1) name of DICOMDIR to create 2) base directory where to start recursing for DICOM files
		found, external_cmd = gmShellAPI.detect_external_binary(dicomdir_cmd)
		if not found:
			_log.error('[%s] not found', dicomdir_cmd)
			return False

		_log.info(u'exporting studies [%s] into [%s]', study_ids, filename)
		sandbox = gmTools.mk_sandbox_dir(prefix = u'dcm-')
		_log.debug(u'sandbox dir: %s', sandbox)
		idx = 0
		for study_id in study_ids:
			study_zip_name = gmTools.get_unique_filename(prefix = u'dcm-', suffix = u'.zip')
			# getting with DICOMDIR returns DICOMDIR compatible subdirs and filenames
			study_zip_name = self.get_study_as_zip_with_dicomdir(study_id = study_id, filename = study_zip_name)
			study_zip = zipfile.ZipFile(study_zip_name)
			# need to extract into per-study subdir because get-with-dicomdir
			# returns identical-across-studies subdirs / filenames,
			idx += 1
			study_unzip_dir = os.path.join(sandbox, 'STUDY%s' % idx)
			# non-beautiful per-study dir name required by subsequent DICOMDIR generation
			study_zip.extractall(study_unzip_dir)
			study_zip.close()
			gmTools.remove_file(study_zip_name)
			_log.debug(u'study [%s] -> %s -> %s', study_id, study_zip_name, study_unzip_dir)

		# create DICOMDIR across all studies,
		# we simply ignore the already existing per-study DICOMDIR files
		target_dicomdir_name = os.path.join(sandbox, 'DICOMDIR')
		gmTools.remove_file(target_dicomdir_name, log_error = False)	# better safe than sorry
		_log.debug('generating [%s]', target_dicomdir_name)
		cmd = u'%(cmd)s %(DICOMDIR)s %(startdir)s' % {
			'cmd': external_cmd,
			'DICOMDIR': target_dicomdir_name,
			'startdir': sandbox
		}
		success = gmShellAPI.run_command_in_shell (
			command = cmd,
			blocking = True
		)
		if not success:
			_log.error('problem running [gm-create_dicomdir]')
			return False
		# paranoia
		try:
			io.open(target_dicomdir_name)
		except StandardError:
			_log.error('[%s] not generated, aborting', target_dicomdir_name)
			return False

		studies_zip = shutil.make_archive (
			gmTools.fname_stem_with_path(filename),
			'zip',
			root_dir = gmTools.parent_dir(sandbox),
			base_dir = gmTools.dirname_stem(sandbox),
			logger = _log
		)
		_log.debug(u'archived all studies with one DICOMDIR into: %s', studies_zip)
		# studies can be _large_ so attempt to get rid of intermediate files
		gmTools.rmdir(sandbox)
		return studies_zip

	#--------------------------------------------------------
	# on-server API
	#--------------------------------------------------------
	def protect_patient(self, orthanc_id):
		url = u'%s/patients/%s/protected' % (self.__server_url, orthanc_id)
		if self.__run_GET(url) == 1:
			return True
		_log.warning(u'patient [%s] not protected against recycling, enabling protection now', orthanc_id)
		self.__run_PUT(url = url, data = 1)
		if self.__run_GET(url) == 1:
			return True
		_log.error(u'cannot protect patient [%s] against recycling', orthanc_id)
		return False

	#--------------------------------------------------------
	def modify_patient_id(self, old_patient_id, new_patient_id):
		pass

	#--------------------------------------------------------
	# upload API
	#--------------------------------------------------------
	def upload_dicom_files(self, files=None):
		pass

	#--------------------------------------------------------
	def upload_from_directory(self, directory=None, search_subdirectories=False):
		pass

	#--------------------------------------------------------
	def upload_with_DICOMDIR(self, DICOMDIR=None):
		pass

	#--------------------------------------------------------
	# helper functions
	#--------------------------------------------------------
	def get_studies_list_by_orthanc_patient_list(self, orthanc_patients=None):
		studies_by_patient = []
		for pat in orthanc_patients:
			pat_dict = {
				'orthanc_id': pat['ID'],
				'name': pat['MainDicomTags']['PatientName'],
				'date_of_birth': pat['MainDicomTags']['PatientBirthDate'],
				'gender': pat['MainDicomTags']['PatientSex'],
				'external_id': pat['MainDicomTags']['PatientID'],
				'studies': []
			}
			studies_by_patient.append(pat_dict)
			o_studies = self.__run_GET(url = u'%s/patients/%s/studies' % (self.__server_url, pat['ID']))
			if o_studies is False:
				_log.error('cannot retrieve studies')
				return []
			for o_study in o_studies:
				study_dict = {
					'orthanc_id': o_study['ID'],
					'date': o_study['MainDicomTags'][u'StudyDate'],
					'time': o_study['MainDicomTags'][u'StudyTime'],
					'series': []
				}
				try:
					study_dict['description'] = o_study['MainDicomTags'][u'StudyDescription']
				except KeyError:
					study_dict['description'] = None
				pat_dict['studies'].append(study_dict)
				for o_series_id in o_study['Series']:
					o_series = self.__run_GET(url = u'%s/series/%s' % (self.__server_url, o_series_id))
					if o_series is False:
						_log.error('cannot retrieve series')
						return []
					series_dict = {
						'orthanc_id': o_series['ID'],
						'date': o_series['MainDicomTags']['SeriesDate'],
						'modality': o_series['MainDicomTags']['Modality'],
						'instances': len(o_series['Instances'])
					}
					try:
						series_dict['time'] = o_series['MainDicomTags']['SeriesTime']
					except KeyError:
						series_dict['time'] = None
					try:
						series_dict['body_part'] = o_series['MainDicomTags']['BodyPartExamined']
					except KeyError:
						series_dict['body_part'] = None
					study_dict['series'].append(series_dict)
		return studies_by_patient

	#--------------------------------------------------------
	def __run_GET(self, url=None, data=None):
		if data is None:
			data = {}
		params = u''
		if len(data.keys()) > 0:
			params = u'?' + urlencode(data)
		full_url = url + params
		try:
			response, content = self.__conn.request(full_url, 'GET')
		except httplib.ResponseNotReady:
			_log.exception('cannot GET: %s', full_url)
			return False
		except socket.error:
			_log.exception('cannot GET: %s', full_url)
			return False

		if not (response.status in [ 200 ]):
			_log.error('cannot GET: %s', full_url)
			_log.error('response: %s', response)
			return False
		try:
			return json.loads(content)
		except StandardError:
			return content

	#--------------------------------------------------------
	def __run_POST(self, url=None, data=None, contentType=u''):
		if isinstance(data, str):
			body = data
			if len(contentType) != 0:
				headers = { 'content-type' : contentType }
			else:
				headers = { 'content-type' : 'text/plain' }
		else:
			body = json.dumps(data)
			headers = { 'content-type' : 'application/json' }
		try:
			response, content = self.__conn.request(url, 'POST', body = body, headers = headers)
		except httplib.ResponseNotReady:
			_log.exception('cannot POST: %s', full_url)
			return False
		except socket.error:
			_log.exception('cannot POST: %s', full_url)
			return False

		if response.status == 404:
			_log.debug('no data, response: %s', response)
			return []
		if not (response.status in [ 200, 302 ]):
			_log.error('cannot POST: %s', url)
			_log.error('response: %s', response)
			return False
		try:
			return json.loads(content)
		except StandardError:
			return content

	#--------------------------------------------------------
	def __run_PUT(self, url=None, data=None, contentType=u''):
		if isinstance(data, str):
			body = data
			if len(contentType) != 0:
				headers = { 'content-type' : contentType }
			else:
				headers = { 'content-type' : 'text/plain' }
		else:
			body = json.dumps(data)
			headers = { 'content-type' : 'application/json' }
		try:
			response, content = self.__conn.request(url, 'PUT', body = body, headers = headers)
		except httplib.ResponseNotReady:
			_log.exception('cannot PUT: %s', full_url)
			return False
		except socket.error:
			_log.exception('cannot PUT: %s', full_url)
			return False

		if response.status == 404:
			_log.debug('no data, response: %s', response)
			return []
		if not (response.status in [ 200, 302 ]):
			_log.error('cannot PUT: %s', url)
			_log.error('response: %s', response)
			return False
		try:
			return json.loads(content)
		except StandardError:
			return content


#============================================================
# orthanc RestToolBox.py (for reference, not in use):
#============================================================
_credentials = None

def SetCredentials(username, password):
    global _credentials
    _credentials = (username, password)

def _SetupCredentials(h):
    global _credentials
    if _credentials != None:
        h.add_credentials(_credentials[0], _credentials[1])


def DoDelete(uri):
    h = httplib2.Http()
    _SetupCredentials(h)
    resp, content = h.request(uri, 'DELETE')

    if not (resp.status in [ 200 ]):
        raise Exception(resp.status)
    else:
        try:
            return json.loads(content)
        except:
            return content



#============================================================
# main
#------------------------------------------------------------
if __name__ == "__main__":

	if len(sys.argv) == 1:
		sys.exit()

	if sys.argv[1] != 'test':
		sys.exit()

#	if __name__ == '__main__':
#		sys.path.insert(0, '../../')
	from Gnumed.pycommon import gmLog2

	#--------------------------------------------------------
	def orthanc_console(host, port):
		orthanc = cOrthancServer()
		if not orthanc.connect(host, port, user = None, password = None):		#, expected_aet = 'another AET'
			print('error connecting to server:', orthanc.connect_error)
			return False
		print('Connected to Orthanc server "%s" (AET [%s] - version [%s] - DB [%s])' % (
			orthanc.server_identification['Name'],
			orthanc.server_identification['DicomAet'],
			orthanc.server_identification['Version'],
			orthanc.server_identification['DatabaseVersion']
		))
		print('')
		print('Please enter patient name parts, separated by SPACE.')

		while True:
			entered_name = gmTools.prompted_input(prompt = "\nEnter person search term or leave blank to exit")
			if entered_name in ['exit', 'quit', 'bye', None]:
				print("user cancelled patient search")
				break

			pats = orthanc.get_patients_by_external_id(external_id = entered_name)
			if len(pats) > 0:
				for pat in pats:
					print(pat)
				continue

			pats = orthanc.get_studies_list_by_patient_name(name_parts = entered_name.split(), fuzzy = True)
			for pat in pats:
				print(pat['name'])
				for study in pat['studies']:
					print(u' ', gmTools.format_dict_like(study, relevant_keys = ['orthanc_id', 'date', 'time'], template = u'study [%%(orthanc_id)s] at %%(date)s %%(time)s contains %s series' % len(study['series'])))
					for series in study['series']:
						print(u'  ', gmTools.format_dict_like(series, relevant_keys = ['orthanc_id', 'date', 'time', 'modality', 'instances', 'body_part'], template = u'series [%(orthanc_id)s] at %(date)s %(time)s: %(modality)s of body part "%(body_part)s" holds %(instances)s images'))
				#print(orthanc.get_study_as_zip_with_dicomdir(study_id = study['orthanc_id'], filename = 'study_%s.zip' % study['orthanc_id']))
				#print(orthanc.get_study_as_zip(study_id = study['orthanc_id'], filename = 'study_%s.zip' % study['orthanc_id']))
				#print(orthanc.get_studies_as_zip_with_dicomdir(study_ids = [ s['orthanc_id'] for s in pat['studies'] ], filename = 'studies_of_%s.zip' % pat['orthanc_id']))
				print(u'--------')

	#--------------------------------------------------------
	try:
		host = sys.argv[2]
		port = sys.argv[3]
	except IndexError:
		host = None
		port = '8042'
	orthanc_console(host, port)