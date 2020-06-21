**The script is to grep each tag with the given search string.**

**Usage:**
*Intall the requirements.txt*
*run main.py*

we need to provide the **repository name** and **search string** to execute the script.
Note: repository name = *usename/repo_name*	

It clone the repo to **repos** directory and provides **json data** in the below format in the current working directory

```JSON
{
"uuid": <ID>,
"component": <REPO_NAME>,
"search_string": <SEARCH STRING>,
"result": <RESULTs>,
"file_path": <IN WHICH FILE THE ABOVE RESULTS EXISTED>,
"reference": <REFERENCE GITHUB URL>
}
```
