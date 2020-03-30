"""
Various parsers for query form input
"""

from mgipython.error import InvalidStageInputError

def emapaStageParser(input):
    """
    parse input into list of theiler stages
    
    Valid inputs are:
        1) single stage "1" or "10"
        2) list "1,2,3" or "10, 11, 20"
        3) range "1-20"
        4) all stages "*"
    """
    stages = []
    
    if input:
        
        input = input.lower()
        
        # check for wildcard
        if "*" in input \
            or "all" in input:
            
            return list(range(1, 29))
        
        # split on comma, then parse each token
        commaSplit = input.split(",")
        
        tokens = []
        
        for token in commaSplit:
            
            token = token.strip()
            if token:
                
                # resolve range input
                if "-" in token:
                    dashSplit = token.split("-")
                    
                    # cannot have more than two operands
                    if len(dashSplit) != 2:
                        msg = "invalid range input: %s" % (token)
                        raise InvalidStageInputError(msg)
                    
                    left = dashSplit[0].strip()
                    right = dashSplit[1].strip()
                    
                    # left and right must not be whitespace
                    if not left and right:
                        msg = "invalid range input: %s" % (token)
                        raise InvalidStageInputError(msg)
                    
                    # left and right must be integers
                    try:
                        leftStage = int(left)
                        rightStage = int(right)
                    except ValueError as ve:
                        raise InvalidStageInputError(ve.message)
                    
                    # left must not be greater than right
                    if leftStage > rightStage:
                        msg = "invalid range input %d > %d: %s" % (leftStage, rightStage, token)
                        raise InvalidStageInputError(msg)
                    
                    # IFF range input is valid, we add the range of values
                    for stage in range(leftStage, rightStage + 1):
                        tokens.append(stage)
               
                else:
                    tokens.append(token)
        
        
        seen = set([])
        for stage in tokens:
        
            try:
                stage = int(stage)
            except ValueError as ve:
                raise InvalidStageInputError(ve.message)
            
            # only add distinct list of stages
            if stage in seen:
                continue
            seen.add(stage)
            
            stages.append(stage)
    
    return stages



def parse_jnumber(input):
    """
    Valid inputs are 
    J:1234
    J1234
    1234
    
    returns valid jnumid format (e.g. J:1234)
    """
    jnumber = input.lower()
        
    if jnumber.startswith("j:"):
        jnumber = jnumber[2:]
        
    elif jnumber.startswith("j"):
        jnumber = jnumber[1:]
        
    if jnumber:
        jnumber = "J:" + jnumber
        
    return jnumber

def splitCommaInput(param):
    """
    split input on comma
    returns lists of inputs
    """
    tokens = []
    splitTokens = param.split(',')
    for token in splitTokens:
        tokens.append(token.strip())
    return tokens



def splitSemicolonInput(input):
    """
    Splits input on semicolon, and returns list of inputs
    """
    inputs = []
    tokens = input.split(';')
    for token in tokens:
        inputs.append(token.strip())
    return inputs
