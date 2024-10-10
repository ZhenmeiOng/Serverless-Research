# Testcase 1 

- Attempting to run test case 1 of Serverless Bench
    - **Together Version (`together.py`):** The whole application is a single serverless function. It connects to S3, downloads data, and performs calculations all within one function.
    - **Split Version (`keyDownloader.py` and `alu.py`):** The application is split into two functions. One function (`keyDownloader.py`) handles downloading data from S3, and the other function (`alu.py`) performs calculations. They work in sequence, where the first function’s output is used by the second function.

- Purpose: to test whether combining or separating tasks uses CPU more efficiently
- can be done by comparing executing time of `together` function with `keyDownloader` and `alu`.
- Try: modify the codes to compare the memory usage between the two versions

### To run the testcase 1 in OpenFaas:
- running together.py
`echo "" | faas-cli invoke together`
- running keydownloader and then alu
```
# invoking keyDownloader and alu:
result=$(echo "" | faas-cli invoke keyDownloader)
#use the result to invoke alu
echo $result | faas-cli invoke alu
```

