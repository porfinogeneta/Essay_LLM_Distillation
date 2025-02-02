prompt = """Summarise the information by selecting and reporting the main features, make comparisons where relevant.
The essay part should consist of MAXIMALLY 190 words!!! 
Use IELTS Academic Band 9 vocabulary.
Avoid repetition.
Don't replicate provided Examples!
Use given structured output:
    1. Graph description
    2. Body paragraphs (2-3 separate paragraps)
    3. Overview of the data


Example 1.

<TITLE_1>: "Changes in population in India and China 2000-2050"
[IMAGE_1]

Follow given structured input:
1. <Describe a graph:>
"The graph gives information about population growth in China and India from the year 2000 with predicted changes to 2050."

2. <Find the key points and trends:>

Paragraph 1:
"In 2000, China’s population stood at 1.25 billion and this number rose steadily to where it is currently at around 1.35 billion. It is projected to peak at 1.45 billion in 2025, when the number will level off and start to decline. It is expected that by 2050 the population will have dropped slightly to 1.4 billion."

Paragraph 2: 
"In contrast, although the population of India started at just one billion in 2000, it has increased rapidly to just under 1.25 billion today. The data indicate it will continue its upward surge, overtaking China in 2030 and reaching a peak of 1.6 billion by 2050."

3. <Write a summary of presented data:>
"Overall, the major difference between the two population trends is that the number of people in China is forecast to start falling after 2030 whereas the population of India will continue to soar."

Example 2.

<TITLE_2>: "Sales of the three most commonly purchased items in a particular bakery for the year 2014."
[IMAGE_2]

Follow given structured input:
1. <Describe a graph:>
"The graph shows the value of sales of popular baked goods in an individual bakery in 2014"

2. <Find the key points and trends:>

Paragraph 1: 
"In January, sales of bread were valued at $80,000 but this figure fell to around $45,000 in March and fluctuated between $40,000 and $65,000 until September. The last quarter, however, saw a jump in the value of bread sales to finish where it was at the beginning of the year."

Paragraph 2: 
"The sales of buns followed quite a different pattern. In January, bun sales stood at $40,000 but quickly rose to $70,000 in May and remained stable until August, after which they plunged to just $30,000 in December."

Paragraph 3:
"The sales of buns followed quite a different pattern. In January, bun sales stood at $40,000 but quickly rose to $70,000 in May and remained stable until August, after which they plunged to just $30,000 in December."

3. <Write a summary of presented data:>
"The value of pies sold slowly increased from $10,000 in January to reach $20,000 in August. Sales then levelled off but went up sharply in the last two months of the year to close just ahead of buns at $40,000. Pies were the only item where sales figures in December exceeded those in January."


Answer.

<TITLE_LAST>: "{title}"
[{image_name}].
Follow given structured input:"""