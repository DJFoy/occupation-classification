# occupation-classification
Classification of occupations using the SOC 2010 (ONS) dataset<p>

This project aims to create a classification tool using the Standard Occupational Classification dataset published by the ONS. This dataset contains 28,573 occupations split into;<br>
  9 major groups<br>
  25 sub-major groups<br>
  90 minor groups<br>
  369 unit groups<p>

The data from the SOC needs to be grouped to create corpuses for the natural language programming. In order to reduce variability of words with similar semantic value, the tokens need to be stemmed, such that 'teacher' and 'teaching' will be counted as one stem, 'teach'.<p>
NLTK and Enchant are used to assist with the collection and cleansing of the occupations.<p>
Once grouped and cleansed, the terms are counted for each group and TF-IDF values are calculated.<p>
Query terms then need to be cleansed in the same manner as the input data in order to calculate a corresponding TF-IDF value and identify the appropriate classification.
