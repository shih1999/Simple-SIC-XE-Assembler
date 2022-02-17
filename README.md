# Simple-SIC-XE-Assembler
Introduction : final project of system programming course.

### A. Basic Information
- Basic 2-pass assembler
- OS : Windows 10
- Language : Python 3.9.1
- Files : source.txt , pass1.py , pass2.py , OPTAB.py

  ![](https://i.imgur.com/c6IZbzR.jpg)

### B. How to Run
``` python =
$ python3 pass1.py
$ python3 pass2.py
```
1. 執行 pass1.py
2. 輸入 source code 檔名

   ![](https://i.imgur.com/PquCb6l.jpg)
3. assembler 開始執行 PASS 1
4. PASS 1 結束後
     - 產生 SYMTAB.json 與 intermediate_file.txt
 
        ![](https://i.imgur.com/8QN7vx0.jpg)

     - 程式自動印出 SYM_TABLE 與 Intermediate File 內容

        ![](https://i.imgur.com/JKvwMTb.jpg)
        ![](https://i.imgur.com/BwkbH00.jpg)

5. 執行 pass2.py
6. assembler 開始執行 PASS 2
7. PASS 2 結束後
     - 產生 result_file.txt 與 object_code.txt

        ![](https://i.imgur.com/nYZpvG3.jpg)

     - 程式自動印出 Result File 與 Object Code File 內容

        ![](https://i.imgur.com/tKVngqN.jpg)
        ![](https://i.imgur.com/RnHx484.jpg)

### C. Data Structure

#### Hash Table

1. OPTAB
   - assembler 內建
   - 以 Dictionary 儲存在 OPTAB.py 中
   - key : Instruction 名稱
   - value : Instruction Opcode, Length
   - example

      ![](https://i.imgur.com/zrh9xdt.jpg)
      
2. REGTAB
    - assembler 內建
    - 以 Dictionary 儲存在 OPTAB.py 中
    - key : Register 名稱
    - value : Register 編號
    - example

      ![](https://i.imgur.com/gKnafTN.jpg)
      
3. SYMTAB
   - PASS 1 產生
   - 以 Dictionary 儲存在 SYMTAB.json 中
   - key : Label
   - value : Location
   - example

      ![](https://i.imgur.com/zG3ddHm.jpg)
      
#### PASS 1
- **Functions :** write_intermediate() , process_line() , print_pass1() , print_SYMTAB() , print_intermediate()
- Read line by line from source file
- Parse each line to get lable , instruction , target
  - line.split()
  - use line length and check positions
- Determine instruction
- call process_line()
  - use write_intermediate() to write line with location imformation into intermediate file
  - add label and its location into symbol table
- Use print_pass1() to print result
  - print_SYMTAB()
  - print_intermediate() 

#### PASS 2
- **Functions :** twosComplement() , get_op() , get_result_1() , get_result_2() , get_disp() , write_file() , write_record() , print_result() , print_obcode() , print_pass2()
- Read line by line from intermediate file
- Parse each line to get location , lable , instruction , target
  - line.split()
  - use line length and check positions 
- Determine instruction ( flag n , flag i )
- Use get_op() to get instruction op
- Use get_disp() to get intruction disp ( flag b , flag p )
- Check for '+' in instruction, '#' or '@' in target ( flag e , flag n , flag i )
- Use get_result_1() for format 3 and get_result_2() for format 4 to generate obcode
- Use write_file() to write into result file
- Use write_record() to write into obcode file
  - if number of obcode > 9 , next T record
  - if loc between two obcode too big ( I use > 4) , next T record
- Use print_pass2() to print result
  - print_result()
  - print_obcode()

### D. Copyright Claim

- This code is written by Shih-Jieh Chen.
- All rights reserved.
- Date : 2022/01/20
