**Author:**           Henry Steele, Library Technology Services, Tufts University
**Name of Program:**  Citations
**Files:**			  processCitations.py, scripts/functions.py
**Date created:**     2018-12

**Purpose:**
  - To create a series of word documents that contain bibliographies of all the Titles
	purchased in a given fiscal year for a given library (Tisch or Ginn)
  - This github repo is in the Tufts University github.com organization at https://github.com/TuftsUniversity/gift-fund-bibliography 
  

**Command:** 
  - retrieve secrets.py from https://tufts.box.com/s/lf6jmsccox8yoyjoavjruxt8zxk0n4wm and install in top level directory
  - install requirements (first time)
	  - python3 -m pip install -r requirements.txt
  - run
	  - python3 processCitations.py
**Method:**
  - provide library and fiscal year prompt
  - program retrives the appropriate Analytics report:
	  - either/or
		  - /shared/Tufts University/Reports/Collections/Gift Funds/Titles Purchased with Gift Funds - Tisch - Generic for Script
		  - /shared/Tufts University/Reports/Collections/Gift Funds/Titles Purchased with Gift Funds - Ginn - Generic for Script
	  - outputs:
		  - MMS Id
		  - fund
	  - filters on
		  - "MMS Id is not equal to / is not in  -1"
		  - (Tisch) "AND Fund Ledger Code is equal to / is in  dalex; dalel; daron; dbarr; dcamp; dchri; dcros; dduke; dfitc; dgiff; dgonz; dgord; dhaly; dharo; dloeb; dmeas; dnewh; dpall; dprit; drose; drosg; dshap; dsper; dtisc; dwill; dfox; docon; dcohe; dargo; dblak; dmarc"
		  - OR (Ginn) "Fund Ledger Name is equal to / is in  Bradley - Books; Cabot - Books; Fares - Books; Hay - Books; Imlah - Books; Maney - Books; Raanan - Books; Salacuse - Books; Saskawa-NPP - Books"
		  - "AND Transaction Date is prompted"
			  - this is passed as a 'saw' XML filter in the URL that encodes the date range
  - retrieves the XML report, iterates through and parses MMS Id and fund
  - performs an SRU search by MMS Id
  - parses out relevant title, author, and pulication information field from bib XML
	  + MMS Id
	  + Main entry Author (MARC 100|a)
	  + Main entry Author relator (MARC 100|e)
	  + Second author (MARC 110|a)
	  + Second author relator (MARC 110|e)
	  + Corporate author (MARC 700|a)
	  + Corporate author relator (MARC 700|e)
	  + Second corporate author (MARC 710|a)
	  + Second corporate author relator (MARC 710|e)
	  + Title (MARC 245|a)
	  + Subtitle (MARC 245|b)
	  + Place of publication (MARC 260|a)
	  + Name of publisher (MARC 260|b)
	  + Date of publication (MARC 260|c)
	  + Place of second publication (MARC 264|a)
	  + Name of second publisher (MARC 264|b)
	  + Date of second publication (MARC 264|c)
  - turns this data into a ".bib" BibTex-style file
  - uses locally python-citeproc "pseudo LaTex" to create bibliography, and docx module to write these to Word


**Dependences:**
  - in "requirements.txt"
      + django<2
	  + pandas
	  + openpyxl
	  + tk
	  + numpy
	  + future
	  + lxml
	  + python-docx
	  + citeproc-py


**Output:**
  - "/Processing/*" directory contains intermediate ".bib" file, which is in BibTex that citeproc
  - "/Output/*" directory contains final Word .docx file
  
**links.py:**
 - For the second object in this process, there’s a Python script called links.py that retrieves an Analytics report of MMS Ids (and fund codes) and uses the MMS Id to construct a Primo URL that can be used for linking on the library websites.   Also configured for either Tisch or Ginn and the specified fiscal year based on prompts.
  
