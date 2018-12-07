# -*- coding: utf-8 -*-
import wolframalpha


appid='5W264Y-2RWYE4Q9T2'
client = wolframalpha.Client(appid)
def getResult(eq):
	res=client.query(eq)
	if res['@success'] == 'false':
		print('Equation cannot be resolved')
  # Wolfram was able to resolve question
	else:
		result = ''
	    # pod[1] may contains the answer
		try:
		    pod1 = res['pod'][1]
		    pod2 = res['pod'][2]
		    pod3 = res['pod'][3]
		except:
			pod1 = res['pod'][1]
	    # checking if pod1 has primary=true or title=result|definition
#		print("pod1=",pod1)
#		print("pod2=",pod2)
#		print("pod=",pod3)
		try:
			if (('definition' in pod1['@title'].lower()) or 
			  ('result' in  pod1['@title'].lower()) or 
			  ('complex solutions' in  pod3['@title'].lower()) or 
			  ('solution' in  (pod2['@title'].lower()) or 
			 ('solution' in  pod3['@title'].lower())) or 
			 (pod1.get('@primary','false') == 'true')):
				# extracting result from pod1
				if ('result' in  pod1['@title'].lower()):
					result = resolveListOrDict(pod1['subpod'])
				elif ('solution' in  pod2['@title'].lower()):
					result = resolveListOrDict(pod2['subpod'])
				elif ('solution' in  pod3['@title'].lower()):
					try:
						result=pod3['subpod'][0]["plaintext"]+', '+pod3['subpod'][1]["plaintext"]+ ', '+pod3['subpod'][2]["plaintext"]
					except:
						try:
							result=pod3['subpod'][0]["plaintext"]+', '+pod3['subpod'][1]["plaintext"]
						except:	
							result=resolveListOrDict(pod3['subpod'])
#				elif ('solution' in  pod3['@title'].lower()):
					
				elif ('complex solutions' in  pod3['@title'].lower()):
					result=pod3['subpod'][0]["plaintext"]+', '+pod3['subpod'][1]["plaintext"]
				print(result)
			else:
				print("Unable to Solve Equation!!")
		except:
			print("Unable to Solve Equation!!")
def resolveListOrDict(variable):
	if isinstance(variable, list):
		return variable[0]["plaintext"]
	else:
		return variable["plaintext"]
getResult("x3 + 9x = 0")