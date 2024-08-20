# lamp-manager
A one-click manager to start, stop or restart **apache2** and **mysql** services via GUI or tray and easily monitor their status.
 
There is also multi-language support: initially Russian and English are available, but it is possible to add other languages yourself.

How to use
---
It's very simple. After installing the required modules, just run the **main.py** file.

The interface is self-explanatory. There is a menu at the top where you can disable minimizing the program to tray (enabled by default), as well as a list of available languages. 

![Interface](https://github.com/user-attachments/assets/95f9b15d-d87f-4aea-80a9-6412a0bccbbc)
![Options menu](https://github.com/user-attachments/assets/0da67e59-e79f-453f-a022-03d6b97f8da4)

In the tray you can find an application icon that will display the current status of the services (enabled or not), and from there you can quickly enable or disable them.

Adding new languages
---
There are a few steps to add a language:
1. First you need the **QtLinguist** program, which you can install with the entire PyQt5 suite or find a standalone version. 
2. Run QtLinguist, then open the file **“uncompiled/locales/lang_template.ts”**. It is not necessary to specify the source and target languages, but it is desirable. 
3. Now translate all sections and fields, strictly taking into account the original strings (for example, don't forget the **"\<b>{}\</b>"** format in one of the strings). 
4. When finished, select “Compile as” from the “File” menu and save the resulting translation to the “locales” folder. The file name should correspond exactly to the template **“lang_CODE.qm”**, where **CODE** is the language code (e.g. en or ru). 

The next time you start the program, this language will be available for selection in the menu

Required modules
---
To work properly, you need only **PyQt5**:<br />
```bat
pip install PyQt5
```