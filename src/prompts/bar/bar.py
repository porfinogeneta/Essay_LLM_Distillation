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

<TITLE_1>: "The chart shows the expenditure of two countries on consumer goods in 2010."
[IMAGE_1]

Follow given structured input:
1. <Describe a graph>:
"The chart illustrates the amount of money spent on five consumer goods (cars, computers, books, perfume and cameras) in France and the UK in 2010. Units are measured in pounds sterling."

2. <Find the key points, trends and compare data>:

Paragraph 1:
"In terms of cars, people in the UK spent about £450,000 on this as opposed to the French at £400,000. Similarly, the British expenditure was higher on books than the French (around £400,000 and £300,000 respectively). In the UK, expenditure on cameras (just over £350,000) was over double that of France, which was only £150,000."

Paragraph 2: 
"On the other hand, the amount of money paid out on the remaining goods was higher in France. Above £350,000 was spent by the French on computers which was slightly more than the British who spent exactly £350,000. Neither of the countries spent much on perfume which accounted for £200,000 of expenditure in France but under £150,000 in the UK."

3. <Write a summary of presented data>:
"Overall, the UK spent more money on consumer goods than France in the period given. Both the British and the French spent most of their money on cars whereas the least amount of money was spent on perfume in the UK compared to cameras in France. Furthermore, the most significant difference in expenditure between the two countries was on cameras."

Example 2.

<TITLE_2>: "The chart shows the average household spending pattern for households in three income categories as a proportion of their income."
[IMAGE_2]

Follow given structured input:
1. <Describe a graph>:
"The bar charts show data about computer ownership, with a further classification by level of education, from 2002 to 2010."

2. <Find the key points, trends and compare data>:

Paragraph 1: 
"An analysis of the data by level of education shows that higher levels of education correspond to higher levels of computer ownership in both of those years."

Paragraph 2: 
"In 2002, only around 15% of those who did not finish high school had a computer but this figure had trebled by 2010. There were also considerable increases, of approximately 30 percentage points, for those with a high school diploma or an unfinished college education (reaching 65% and 85% respectively in 2010). However, graduates and postgraduates proved to have the greatest level of ownership in 2010, at 90% and 95% respectively, 20 percentage points higher than in 2002."

Paragraph 3:
"The last decade has seen a substantial growth in computer ownership in general, and across all educational levels."

3. <Write a summary of presented data>:
"A steady but significant rise can be seen in the percentage of the population that owned a computer over the period. Just over half the population owned computers in 2002, whereas by 2010 three out of four people had a home computer."

Answer.

<TITLE_LAST>: "{title}"
[{image_name}].
Follow given structured input:"""