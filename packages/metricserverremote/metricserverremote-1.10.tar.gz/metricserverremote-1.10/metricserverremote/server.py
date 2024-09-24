import array
import base64
import shutil
import zipfile
import zeep
import hashlib
import sys
import os
import datetime
import time
import xml.etree.ElementTree as ET

class MetricServer:
    def __init__(self):
        self.sessionId = None
        self.remoteServer = ""
        self.userName = "admin"
        self.password = "admin"
        self.userclient = None
        self.licenseclient = None
        self.tagsclient = None
        self.resultclient = None
        self.processclient = None
        self.wsdldir = '{}{}{}'.format(os.path.dirname(__file__), os.sep, 'mswsdls')
        self.supported_sample_rates = [8000, 16000, 32000, 44100, 48000]

    def md5hash(self, data):
        md5 = hashlib.md5()
        md5.update(data.encode('utf-8'))
        return md5.hexdigest()

    def logoff(self):
        if self.sessionId is None:
            return
        try:
            self.userservice.Logoff(self.sessionId)
        except zeep.exceptions.Fault as fault:
            print('Logoff error : {}'.format(fault.message))
        except:
            print("Unexpected error:", sys.exc_info()[0])
        self.sessionId = None

    def create_service(self, type, timeout):
        wsdlpath = '{}{}{}'.format(self.wsdldir, os.sep, '{}{}service.wsdl'.format(type,os.sep))
        if not os.path.exists(wsdlpath):
            return 'File {} needed by the python API not found'.format(wsdlpath)
        client = zeep.Client(wsdl=wsdlpath, transport=zeep.Transport(timeout=timeout))
        return self.get_service(client=client)

    def logon(self, server, user, password, timeout=300):
        self.remoteServer = server
        self.userservice = self.create_service('users', timeout)
        self.licenseservice = self.create_service('license', timeout)
        self.tagsservice = self.create_service('tags', timeout)
        self.resultservice = self.create_service('result', timeout)
        self.processservice = self.create_service('processing', timeout)
        self.metricsservice = self.create_service('metrics', timeout)
        self.outputservice = self.create_service('outputconfiguration', timeout)
        self.userName = user
        self.password = password
        try:
            salt_id = self.userservice.InitiateLogon(username=self.userName)
            items = salt_id.split(';')
            hashedpassword = self.md5hash(password)
            ps = self.md5hash(hashedpassword + items[0])
            self.sessionId = self.userservice.CompleteLogon(username=self.userName, hash=ps, clientID=items[1])
        except zeep.exceptions.Fault as fault:
            print('Login error : {}'.format(fault.message))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return 0
        if self.licenseservice.KeyInstalled():
            return 1
        else:
            print("No MetricServer license installed")
            return 0

    def mask(self, output, tags):
        if len(tags) == 0:
            return 0
        header = zeep.xsd.ComplexType([
            zeep.xsd.Element('{http://soap.malden.co.uk}SessionId', zeep.xsd.String()),
        ])
        header_value = header(SessionId=self.sessionId)
        result = self.tagsservice.AddTags(outputConfiguration=output,
                                                 tags=tags,
                                                 _soapheaders=[header_value])

        tagres = 0
        i = 0
        while i < len(result):
            tagres += result[i].Bit
            i += 1
        return tagres

    def __result_from_file_pair_id(self, output, filepairid):
        try:
            header = zeep.xsd.ComplexType([
                zeep.xsd.Element('{http://soap.malden.co.uk}SessionId', zeep.xsd.String()),
            ])
            header_value = header(SessionId=self.sessionId)
            resultid = self.resultservice.ResultIdFromFilePairId(outputConfiguration=output,
                                                                 filePairID=filepairid,
                                                                 _soapheaders=[header_value])
        except zeep.exceptions.Fault as ex:
            return ex.message
        except:
            return 0, sys.exc_info()[0]

        return resultid, ''

    def __result_error(self, output, resultid):
        try:
            header = zeep.xsd.ComplexType([
                zeep.xsd.Element('{http://soap.malden.co.uk}SessionId', zeep.xsd.String()),
            ])
            header_value = header(SessionId=self.sessionId)
            error = self.resultservice.ResultError(outputConfiguration=output,
                                                   resultID=resultid,
                                                   _soapheaders=[header_value])
        except zeep.exceptions.Fault as ex:
            return ex.message
        except AttributeError:
            return ''
        except TypeError as err:
            return sys.exc_info()[0]

        return error

    def processfilepair(self, ref, deg, metric, output, timeout=0, tags=''):
        if self.sessionId is None:
            return 'You must be logged in first'
        if timeout == 0:
            timeout = 60
        #check ref file exists
        exists = os.path.isfile(ref)
        if not exists:
            return ref + "No found"
        # check ref file exists
        exists = os.path.isfile(deg)
        if not exists:
            return deg + "No found"

        if tags != '':
            listags=tags.split('|')
        else:
            listags=[]

        try:
            tagMask = self.mask(output, listags)
            header = zeep.xsd.ComplexType([
                zeep.xsd.Element('{http://soap.malden.co.uk}SessionId', zeep.xsd.String()),
                ])
            header_value = header(SessionId=self.sessionId)
            filepairId = self.processservice.PrepareUpload(metric, output, self.userName, _soapheaders=[header_value])

            with open(ref, "rb") as image_file:
                encoded_stringref = image_file.read()
            with open(deg, "rb") as image_file:
                encoded_stringdeg = image_file.read()
            header = zeep.xsd.ComplexType([
                        zeep.xsd.Element('{http://soap.malden.co.uk}FileName', zeep.xsd.String()),
                        zeep.xsd.Element('{http://soap.malden.co.uk}FilePairID', zeep.xsd.String()),
                        zeep.xsd.Element('{http://soap.malden.co.uk}OutputConfiguration', zeep.xsd.String()),
                        zeep.xsd.Element('{http://soap.malden.co.uk}SessionId', zeep.xsd.String()),
                    ])
            headerref_value = header(FileName=ref, FilePairID=filepairId, OutputConfiguration=output, SessionId=self.sessionId)
            headerdeg_value = header(FileName=deg, FilePairID=filepairId, OutputConfiguration=output, SessionId=self.sessionId)
            self.processservice.UploadReference(Stream=encoded_stringref, _soapheaders=[headerref_value])
            self.processservice.UploadDegraded(Stream=encoded_stringdeg, _soapheaders=[headerdeg_value])

            self.processservice.Process(filepairID=filepairId, output=output, tagMask=tagMask, _soapheaders=[header_value])

            start = datetime.datetime.now()
            if filepairId > 0:
                resultid = -1
                while resultid == -1:
                    resultid, error = self.__result_from_file_pair_id(output, filepairId)
                    elapsed = datetime.datetime.now() - start
                    #print('elapsed : {} and result id : {}'.format(elapsed, resultid))
                    if elapsed.seconds >= timeout:
                        error = 'Timeout when processing file pair'
                        resultid = 0
                    time.sleep(0.2)

                if resultid == 0:
                    return error
                else:
                    resulterror = self.__result_error(output, resultid)
                    if resulterror == '' or resulterror is None:
                        return resultid
                    else:
                        if type(resulterror) is type:
                            print("Warning metric server must be updated")
                            return resultid
                        else:
                            return resulterror
            else:
                isProcessed = False
                error = ""
                while not isProcessed:
                    isProcessed = self.processservice.IsFilePairProcessed(filepairID=filepairId)
                    #print('is processed = {}'.format(isProcessed))
                    time.sleep(0.2)
                    elapsed = datetime.datetime.now() - start
                    if elapsed.seconds >= timeout:
                        error = 'Timeout when processing file pair'
                        isProcessed = True
                if not error:
                    return filepairId
                else:
                    return error
        except zeep.exceptions.Fault as ex:
            return ex.message
        except AttributeError as attrError:
            print('Soap error : {}'.format(attrError))
            return str(attrError)
        except zeep.exceptions.TransportError:
            return 'connection failed, retry login'
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return sys.exc_info()[0]

    def is_integer(self, n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()

    def results(self, output, resultid):
        if self.sessionId is None:
            return 'You must be logged in first'
        try:
            header = zeep.xsd.ComplexType([
                zeep.xsd.Element('{http://soap.malden.co.uk}SessionId', zeep.xsd.String()),
            ])
            header_value = header(SessionId=self.sessionId)
            results = self.resultservice.ResultMeasurements(outputConfiguration=output,
                                                                   resultID=resultid,
                                                                   _soapheaders=[header_value])
            if len(results) == 0:
                return 'No results found for ID : ' + resultid
            newlist = []
            for res in results:
                if self.is_integer(res.Value):
                    elt = [res.Name, res.DisplayName, float(res.Value.replace(',', '.'))]
                else:
                    elt = [res.Name, res.DisplayName, res.Value]
                newlist.append(elt)
            return newlist
        except ValueError:
            return 'cannot convert ' + res.Value + ' to float'
        except zeep.exceptions.Fault as ex:
            return ex.message
        except:
            return sys.exc_info()[0]

    def removedbresult(self, output, resultid):
        if self.sessionId is None:
            return 'You must be logged in first'
        try:
            header = zeep.xsd.ComplexType([
                zeep.xsd.Element('{http://soap.malden.co.uk}SessionId', zeep.xsd.String()),
            ])
            header_value = header(SessionId=self.sessionId)
            return_code = self.resultservice.RemoveResultFromDb(outputConfiguration=output,
                                                                   resultID=resultid,
                                                                   _soapheaders=[header_value])
            if return_code == 0:
                return 0
            if return_code == 1001:
                return 'No results found for ID : ' + resultid
            else:
                return 'unable to remove result for ID : ' + resultid + ". ErrorCode : " + return_code
        except zeep.exceptions.Fault as ex:
            return ex.message
        except:
            return sys.exc_info()[0]

    def saverst(self, output, resultid, path, filename=''):
        if self.sessionId is None:
            return 'You must be logged in first'
        if resultid <= 0:
            return 'Invalid result ID : '+resultid
        if not os.path.isdir(path):
            return 'Destination path : ' + path + ' not found'

        try:
            header = zeep.xsd.ComplexType([
            zeep.xsd.Element('{http://soap.malden.co.uk}SessionId', zeep.xsd.String()),])
            header_value = header(SessionId=self.sessionId)
            messageStream = self.resultservice.ResultFile(outputConfiguration=output, resultID=resultid, _soapheaders=[header_value])
        except zeep.exceptions.Fault as ex:
            return ex.message

        if filename == '':
            fullpath = '{}{}{}.rst'.format(path, os.sep, resultid)
        else:
            fullpath = '{}{}{}.rst'.format(path, os.sep, filename)

        with open(fullpath, 'wb') as f:
            f.write(messageStream)
        return ''

    def exportview(self, output, resultid, path, view, filename=''):
        if filename == '':
            tmprstpath = '{}{}{}.rst'.format(path, os.sep, resultid)
            outfilepath = '{}{}{}.csv'.format(path, os.sep, resultid)
        else:
            tmprstpath = '{}{}{}.rst'.format(path, os.sep, filename)
            outfilepath = '{}{}{}.csv'.format(path, os.sep, filename)
        res = self.saverst(output, resultid, path, filename)
        extract_dir = '{}{}{}'.format(path, os.sep, 'extract')
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        os.mkdir(extract_dir)
        try:
            if res == '':
                with zipfile.ZipFile(tmprstpath, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                views_dir = '{}{}{}'.format(extract_dir, os.sep, 'Views')
                if not os.path.exists(views_dir):
                    return "No Views found for this result"
                else:
                    elements = view.split('/')
                    if len(elements) != 2:
                        return "View parameter must be with format : Group/View"
                    else:
                        group_dir = '{}{}{}'.format(views_dir, os.sep, elements[0])
                        if not os.path.exists(group_dir):
                            return 'group {} not found in views for this result'.format(elements[0])
                        else:
                            xml_path = '{}{}{}.xml'.format(group_dir, os.sep, elements[1])
                            if not os.path.exists(xml_path):
                                return 'view {} not found in group views for this result'.format(elements[1])
                            else:
                                tree = ET.parse(xml_path)
                                data_type = tree.find('type').text
                                #print('view type is {}'.format(data_type))
                                data = tree.find('data').text
                                decoded_bytes = base64.standard_b64decode(data)
                                #print('decoded bytes length = {}'.format(len(decoded_bytes)))
                                if data_type == 'short[]':
                                    shorts = array.array('h')
                                    shorts.frombytes(decoded_bytes)
                                    if elements[1] == 'PesqxClippingEst':
                                        reference = [None] * len(shorts)
                                        degraded = [None] * len(shorts)
                                        front = [None] * len(shorts)
                                        back = [None] * len(shorts)
                                        hangover = [None] * len(shorts)
                                        i = 0
                                        for elt in shorts:
                                            reference[i] = ((shorts[i] & 0x10) >> 4) + 9
                                            degraded[i] = ((shorts[i] & 0x20) >> 5) + 7
                                            front[i] = ((shorts[i] & 0x200) >> 9) + 5
                                            back[i] = ((shorts[i] & 0x400) >> 10) + 3
                                            hangover[i] = ((shorts[i] & 0x1000) >> 12) + 1
                                            i += 1
                                        with open(outfilepath, "w") as outfile:
                                            outfile.write('Hang-over,Back-end,Front-end,Degraded,Reference\n')
                                            i = 0
                                            for elt in hangover:
                                                outfile.write('{},{},{},{},{}{}'.format(hangover[i], back[i], front[i], degraded[i], reference[i], "\n"))
                                                i += 1
                                            return 'Ok'
                                    else:
                                        with open(outfilepath, "w") as outfile:
                                            for elt in shorts:
                                                outfile.write('{}\n'.format(str(elt)))
                                        return 'Ok'
                                else:
                                    if data_type == 'int[]':
                                        ints = array.array('i')
                                        ints.frombytes(decoded_bytes)
                                        with open(outfilepath, "w") as outfile:
                                            for elt in ints:
                                                outfile.write('{}\n'.format(str(elt)))
                                        return 'Ok'
                                    else:
                                        if data_type == 'single[]':
                                            singles = array.array('f')
                                            singles.frombytes(decoded_bytes)
                                            with open(outfilepath, "w") as outfile:
                                                for elt in singles:
                                                    outfile.write('{}\n'.format(str(elt)))
                                            return 'Ok'
            else:
                return res
        except Exception as e:
            return str(e)
        finally:
            shutil.rmtree(extract_dir)
            os.remove(tmprstpath)

    def configureheaderless(self, refSamplerate, refFormat, degSamplerate, degFormat, channel):
        if self.sessionId is None:
            return 'You must be logged in first'
        if refSamplerate not in self.supported_sample_rates:
            return 'Invalid reference Samplerate {}. 8000, 16000, 32000, 44100, or 48000 is expected'.format(refSamplerate)

        if degSamplerate not in self.supported_sample_rates:
            return 'Invalid degraded Samplerate {}. 8000, 16000, 32000, 44100, or 48000 is expected'.format(degSamplerate)

        if refFormat.lower() != 'littleendian' and refFormat.lower() == 'bigendian':
            return 'Invalid reference format {}'.format(refFormat)

        if degFormat.lower() != 'littleendian' and degFormat.lower() == 'bigendian':
            return 'Invalid degraded format {}'.format(degFormat)

        if channel != 1 and channel != 2:
            return 'Only Mono or Stereo supported'

        header = zeep.xsd.ComplexType([
            zeep.xsd.Element('{http://soap.malden.co.uk}SessionId', zeep.xsd.String()),
        ])
        header_value = header(SessionId=self.sessionId)
        try:
            return self.processservice.ConfigureHeaderlessSettings(headerless={'Channel': channel,
                                                                  'ReferenceFormat': refFormat,
                                                                  'ReferenceSampleRate': refSamplerate,
                                                                  'DegradedFormat': degFormat,
                                                                  'DegradedSampleRate': degSamplerate}, _soapheaders=[header_value])
        except zeep.exceptions.Fault as ex:
            return ex.message
        except:
            return sys.exc_info()[0]

    def listheaderlessconfig(self):
        if self.sessionId is None:
            return 'You must be logged in first'
        header = zeep.xsd.ComplexType([
            zeep.xsd.Element('{http://soap.malden.co.uk}SessionId', zeep.xsd.String()),
        ])
        header_value = header(SessionId=self.sessionId)
        result = self.processservice.HeaderlessSettings(_soapheaders=[header_value])
        try:
            return [result.ReferenceSampleRate, str(result.ReferenceFormat),
                    result.DegradedSampleRate, str(result.DegradedFormat),
                    result.Channel]
        except zeep.exceptions.Fault as ex:
            return ex.message
        except:
            return sys.exc_info()[0]


    def listmetricconfigurations(self):
        if self.sessionId is None:
            return 'You must be logged in first'
        header = zeep.xsd.ComplexType([
            zeep.xsd.Element('{http://soap.malden.co.uk}SessionId', zeep.xsd.String()),
        ])
        header_value = header(SessionId=self.sessionId)
        listmetrics = self.metricsservice.List(_soapheaders=[header_value])
        result = []
        for metricconf in listmetrics:
            result.append([metricconf.Name, metricconf.Modified, metricconf.Version, int(metricconf.InUse=='true')])
        return result

    def listoutputconfigurations(self):
        if self.sessionId is None:
            return 'You must be logged in first'
        header = zeep.xsd.ComplexType([
            zeep.xsd.Element('{http://soap.malden.co.uk}SessionId', zeep.xsd.String()),
        ])
        header_value = header(SessionId=self.sessionId)
        listoutput = self.outputservice.List(_soapheaders=[header_value])
        result = []
        for outputconf in listoutput:
            result.append([outputconf.Name,
                           outputconf.DatabaseServer,
                           outputconf.RstFolder,
                           outputconf.CsvFolder,
                           outputconf.CsvFilename,
                           outputconf.Modified,
                           outputconf.Space,
                           int(outputconf.InUse=='true')])
        return result

    def listtags(self, output):
        if self.sessionId is None:
            return 'You must be logged in first'
        header = zeep.xsd.ComplexType([
            zeep.xsd.Element('{http://soap.malden.co.uk}SessionId', zeep.xsd.String()),
        ])
        header_value = header(SessionId=self.sessionId)
        listtags = self.tagsservice.AllTags(outputConfiguration=output, _soapheaders=[header_value])
        result = []
        if listtags is None:
            return result
        for tag in listtags:
            result.append([tag.Bit, tag.Value])
        return result

    def get_service(self, client):
        service_binding = client.service._binding.name
        service_address = client.service._binding_options['address']
        return client.create_service(service_binding, service_address.replace('localhost',self.remoteServer, 1))












