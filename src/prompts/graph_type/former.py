prompt = """
    You have four distinct plot classes: BAR, LINE, PIE, TABLE.
    You task is to answer what type of the plot is the last one provided.

    Examples: 
        [IMAGE_1]
        Given four classes of data: BAR, LINE, PIE, TABLE tell me what is the graph type here.
        Answer: PIE

        [IMAGE_2]
        Given four classes of data: BAR, LINE, PIE, TABLE tell me what is the graph type here.
        Answer: LINE

        [IMAGE_3]
        Given four classes of data: BAR, LINE, PIE, TABLE tell me what is the graph type here.
        Answer: TABLE

        [IMAGE_4]
        Given four classes of data: BAR, LINE, PIE, TABLE tell me what is the graph type here.
        Answer: BAR

    Your task: 
        [{image_name}]
        Given four classes of data: BAR, LINE, PIE, TABLE tell me what is the graph type here.
        Answer: 
""" 