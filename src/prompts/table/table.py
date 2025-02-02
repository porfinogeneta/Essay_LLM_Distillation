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
    
<TITLE_1>: "Standards of living in various countries in 1982."
[IMAGE_1]

Follow given structured input:
1. <Describe a graph:>
"The table uses four economic indicators to show the standard of living in five selected countries in 1982."

2. <Find the key points and trends:>

Paragraph 1:
"To begin, the USA, which is a developed country, had the highest GNP at 13,160 dollars per head.  It also had a much higher daily calorie intake and life expectancy, and the lowest rate of infant mortality, at only 12 per 1000 live births."

Paragraph 2: 
"Quality of life was much lower for the other four countries. The indicators for Egypt, Indonesia and Bolivia were fairly similar, with their GNP ranging from 570 to 690 and daily calories in the 2000s. Life expectancy was also almost the same, although Bolivia had much worse infant mortality at 124 per 1000."

Paragraph 3:
"Bangladesh had by far the lowest quality of life in all the indicators.  Its GNP per head was approximately one percent of the USA’s.  Its calorie intake and life expectancy were about half those of the USA, and its infant mortality rate was 11 times greater."

3. <Write a summary of presented data:>
"Overall, it can be seen that the quality of life in the USA was far higher than the other four countries."

Example 2.

<TITLE_2>: "Underground Railway Systems in various cities."
[IMAGE_2]

Follow given structured input:
1. <Describe a graph:>
"The table displays the date opened, number of kilometers and passengers each year in millions for subway systems in various cities."

2. <Find the key points and trends:>

Paragraph 1: 
"London opened first (1863) and is nearly twice as expansive (394 kilometers) as the second largest subway, in Paris, which opened in 1900 and is 199 kilometers long. However, Paris now has more passengers compared to London (1,191,000,000 to 775,000,000). Tokyo was the next oldest having been constructed in 1927 with routes measuring a total of 155 kilometers and being made use of by 1,928,000,000 passengers annually."

Paragraph 2: 
"The more modern subways are Washington D.C. (1976), Kyoto (1981), and Los Angeles (2001). Washington is the largest of the 3 at 126 kilometers with 144,000,000 yearly passengers. Kyoto is by far the smallest (11 kilometers) and serves relatively few individuals (45 million). Similarly, the Los Angeles subway is 18 kilometers in cumulative length and only 50,000,000 people travel on it each year."

3. <Write a summary of presented data:>
"Looking from an overall perspective, it is readily apparent that the earlier underground railways tend to be longer and now serve more passengers per year relative to the more recent ones. Tokyo stands out for serving by far the most passengers and London for being both the oldest and largest."

Answer.

<TITLE_LAST>: "{title}"
[{image_name}].
Follow given structured input:
"""