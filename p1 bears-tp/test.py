//takes two strings as input, one is the string you're trying to match. the only special character means 0 or more of any chareacter. does the string match the pattern

# bool pattern_matcher( char* string, char* pattern) 
# {
# 	for(int i=0; string[i]!='\0', i++){
# 		if( pattern[i]!= '*'){
# 			if (pattern[i] != string[i])
# 				return false
# 		}
# 		else {
# 			bool nextStep = pattern
# 		}
# 	}
# }

def pattern_matcher(string, pattern):
	if (len(string) == 0)
		return false

	for i in range(0, len(string)):

		if pattern[i] != '*':
			if pattern[i] != string[i]:
				return false
		else:
			return pattern_matcher( string[i+1:], pattern[i:])


			

