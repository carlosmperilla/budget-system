# Budget System

The Budget System allows you to manage dataframe data with store purchase budgets by date.

- It groups the relevant information, the most expensive and the cheapest products in a table.
- Spents per store purchase on a date, per store in a month, per month, per year and total spent.
- It shows this information segmented and colored, both by python code, and by a **command line** application to facilitate visualization.
- The system can be created relatively easily, starting from the budget files, copying them (_by default_) or moving them, as indicated.
- It has a translation system to be able to integrate languages beyond English or Spanish, for the months and the display in your language.
- Cross-platform compatibility.

### Dependencies
Budget System requires three external dependencies.
- [Pandas][pandas install]
 It is to manage the tables through dataframes.
- [Colorama][colorama install]
 It is to color the visualization by console.
- [Numpy][numpy install]
 It is for type float64.

### Instalation
```sh
pip install budget-system
```

## Index
* [Introduction](https://github.com/carlosmperilla/budget-system#introduction)
	* [Pre-requirements](https://github.com/carlosmperilla/budget-system#pre-requirements)
	* [Creation](https://github.com/carlosmperilla/budget-system#creation)
	* [Addition Files](https://github.com/carlosmperilla/budget-system#addition-files)
* [Visualization](https://github.com/carlosmperilla/budget-system#visualization)
* [Data Processing](https://github.com/carlosmperilla/budget-system#data-processing)
	* [Spent](https://github.com/carlosmperilla/budget-system#spent)
		* [ProductsData](https://github.com/carlosmperilla/budget-system#productsdata)
		* [DatesDict](https://github.com/carlosmperilla/budget-system#datesdict)
		* [SectorsDict](https://github.com/carlosmperilla/budget-system#sectorsdict)
		* [MonthData](https://github.com/carlosmperilla/budget-system#monthdata)
		* [YearData](https://github.com/carlosmperilla/budget-system#yeardata)
		* [TotalData](https://github.com/carlosmperilla/budget-system#totaldata)
	* [PurchaseList](https://github.com/carlosmperilla/budget-system#purchaselist)
	* [ParserTableName](https://github.com/carlosmperilla/budget-system#parsertablename)
* [Translation](https://github.com/carlosmperilla/budget-system#translation)
	* [Only translation](https://github.com/carlosmperilla/budget-system#only-translation)
	* [Add a new language](https://github.com/carlosmperilla/budget-system#add-a-new-language)
	* [Add a new language and Translate](https://github.com/carlosmperilla/budget-system#add-a-new-language-and-translate)

## Introduction
### Pre-requirements
* The csv files with the purchase data must have at least one column with the prices of each product.
* The names of each table must have the following format to be identified by the package and correctly located in the Budget System folder tree:
 **whatever_storename_[day-month-year].csv**
    * Example:
     **Purchase_List_Amazon_[14-05-22].csv**
        * Note:
        _There is one subtle exception_: the **date format** can be changed if you want, before creating the **Budget System**. But this option is **not available on the command line**. But in the python script creation format. Please read further if this is what you require.
### Creation
When creating a Budget System. A folder is generated that will contain the specified files, with the following structure:
>base_folder/year/month/file.csv

**Example:** A file with the following name _Purchase_List_NameStoreOne_[23-04-22].csv_ would copy/move to: 
>C:\Users\username\Documents\MyBudget\2022\April\Purchase_List_NameStoreOne_[23-04-22].csv

And a configuration file located in it:
>base_folder/config.ini

Which will contain the _language, the price_name, the date format and the path of the base folder_.

* #### Complete script to create a Budget System:
   ```python
  from budget_system import Budget

  budget_files = [
	    r"C:\Users\username\Documents\GenericFolderOne\Purchase_List_NameStoreOne_[23-04-22].csv",
	    r"C:\Users\username\Downloads\GenericFolderTwo\Purchase_List_NameStoreTwo_[27-02-22].csv",
	    r"C:\Users\username\Desktop\GenericFolderThree\Purchase_List_NameStoreThree_[23-05-23].csv",
	    ]
  context = {
    	"lang" : "ENG",
	    "price_name" : "Price(USD)",
        "base_folder" : r"C:\Users\username\Documents\MyBudget",
        "budget_files" : budget_files,
        "budget_files_action" : "COPY",
        "date_format" : "%d-%m-%y"
    }
    
  budget = Budget(**context)
  budget.create_budget_system()
    ```
    * The original files can be located in different folders.
    * By default, only two languages are available: **English (ENG)** and **Spanish (SPA)**. For other languages see the Translation section.
    * If a language is not specified, it will check if the operating system is configured by default in Spanish or English and choose one of these. Otherwise, it will choose **English as the default language**.
    * **_price_name_** refers to the name of the column that contains the prices.
    * **_base_folder_** refers to the path of the folder that will contain the **Budget System**. If the path does not exist, it creates it.
    * **_budget_files_action_** refers to the action that is carried out with the original files, this can be _MOVE_ or _COPY_. If not specified, the files will be copied.
    * **_date_format_** sets the _date format_, to know how to parse the dates that have the names of the files in square brackets. If not specified, defaults to **day-month-year**. [More about date formats in Python][date format python].


* #### Command line for create a Budget System:
   ```sh
  budgetsys --create ENG Price(USD) C:\Users\username\Documents\MyBudge COPY Files C:\Users\username\Documents\GenericFolderOne\Purchase_List_NameStoreOne_[23-04-22].csv C:\Users\username\Downloads\GenericFolderTwo\Purchase_List_NameStoretwo_[27-02-22].csv
   ```
   * **-\-create** can be reduced to **-c** .
   * The arguments are required, **not optional**. In order they are _Language, Price_Name, Base_Folder, Budget_Files_Action_.
   * **Files** indicates that the following are the paths to the **original budget files**
   * Note that there is no option for date format. This is because the command line is meant for quick actions. **To set date format, use a python script and import Budget**

### Addition Files
Once the system is created, later we will need to add new files. For this there are the following options.
This will create the necessary folder structure, and copy or move the files as indicated.

* #### Complete script for add files to Budget System:
   ```python
  import os
  from budget_system import Budget
  
  budget_files = [
	    r"C:\Users\username\Documents\GenericFolderOne\Purchase_List_NameStoreTwo_[12-04-22].csv",
	    r"C:\Users\username\Downloads\GenericFolderTwo\Purchase_List_NameStoreFour_[01-07-22].csv",
	    ]
  context = {
      "base_folder" : r"C:\Users\username\Documents\MyBudget",
      "budget_files" : budget_files,
      "budget_files_action" : "COPY",
            }
  
  # We set the environment variable to contain the configuration set at system creation.
  os.environ['CONFIG_BUDGET'] = os.path.join(context["base_folder"], 'config.ini')
  
  budget = Budget(**context)
  budget.add_budget_files()
   ```
    * You must set the environment variable **CONFIG_BUDGET** to the location of the configuration file either from the **_shell_**, or as in this case **_directly from the script_**. I recommend this second form.
    * **_budget_files_action_** If not specified, the files will be copied.
    
    
* #### Command line for add files to Budget System:
  ```sh
  budgetsys --add C:\Users\carlo\Desktop\pruebitas COPY Files C:\Users\username\Downloads\GenericFolderTwo\Purchase_List_NameStoreFour_[01-07-22].csv
  ```
    * You must set the **CONFIG_BUDGET** environment variable from the shell. Before executing the command.
   * **-\-add** can be reduced to **-a** .
   * The arguments are required, **not optional**. In order they are Base_Folder, Budget_Files_Action_.
   * **Files** indicates that the following are the paths to the **original budget files**

## Visualization
The Budget System package has an internal method for displaying data. The display hierarchy is as follows:
> **Total Data** --> **Year Data** --> **Month Data** --> **Store Data** --> **Store-Date Data**

* **Total Data:** Contains all the following hierarchies. And the total spent.
* **Year Data:** Contains all the following hierarchies. And the year spent.
* **Month Data:** Contains all the following hierarchies. And the month spent.
* **Store Data:** Contains one or multiple _dates_ with the basic data.
* **Date Data:** Contains the basic data, _spent_ of the day of purchase, 3 _most expensive_ products and 3 _cheapest_ products.

If you need to process the data in another way, I recommend that you read **Data Processing**, later, about the **Spent** class.

If what you require is a quick, color-coded view of expenses, this is the tool for you.

There are two ways to display the data, the recommended one is by command line with **budgetsys**, and the other is using the **DisplayData** class.

For both cases, the environment variable **CONFIG_BUDGET** must have been set beforehand with the location of the Budget System configuration file.

#### Example of visualization of Total Data:
![Budget System Display Total Data](https://raw.githubusercontent.com/carlosmperilla/budget-system/main/example%20imgs/budget_system_example_1.PNG)

#### Before starting
You must set the environment variable **CONFIG_BUDGET**, with the location of the Budget System configuration file created **_config.ini_**

### Command-Line or Script
* #### Command-Line
    * ##### Display Total Data:
      It receives no arguments and displays the information for all years.
      ```sh
      budgetsys -dt
      ```
      * The extended argument is **-\-displaytotal**
    * ##### Display Year Data:
      This receives a single, int argument corresponding to the **year**. 
      ```sh
      budgetsys -dy 2022
      ```
      * The extended argument is **-\-displayyear**
    * ##### Display Month Data:
      This receives two arguments, the first int, corresponding to the **year**. The second a **month**(int or string).
      
      ```sh
      budgetsys -dm 2022 4
      ```
      ```sh
      budgetsys -dm 2022 April
      ```
      * The extended argument is **-\-displaymonth**  
    * ##### Display Store (sector) Data:
      This receives three arguments, the first numeric, corresponding to the **year**. The second to the **month**(int or string). The third the **name of the store** in the title of the files for that month.
      
      ```sh
      budgetsys -ds 2022 4 StoreOne
      ```
      ```sh
      budgetsys -ds 2022 April StoreOne
      ```
      * The extended argument is **-\-displaysector**
    * ##### Display Date (sector-date) Data:
      This receives four arguments, the first numeric, corresponding to the **year**. The second to the **month**(int or string). The third the **name of the store** in the title of the files for that month. And the fourth to the **date of purchase in that store**.
      
      ```sh
      budgetsys -dd 2022 4 StoreOne 23-04-22
      ```
      ```sh
      budgetsys -dd 2022 April StoreOne 23-04-22
      ```
      * The extended argument is **-\-displaysectordate**
* #### Script
  If you want to access the display functions without using the command line, you should use the Spent class.
    * ##### Display Total Data:
      ```python
      import os
      from budget_system import DisplayData
      
      base_folder = r"C:\Users\username\Documents\MyBudget"
  
      #If the environment variable for the configuration has not been set, we set it.
      if not os.environ.get('CONFIG_BUDGET'):
        os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')
  
      DisplayData().show_total_data()
      ```
    * ##### Display Year Data:
      ```python
      import os
      from budget_system import DisplayData, Spent
      
      base_folder = r"C:\Users\username\Documents\MyBudget"
  
      #If the environment variable for the configuration has not been set, we set it.
      if not os.environ.get('CONFIG_BUDGET'):
        os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')
  
      year = 2022
      data_years = Spent().spending_by_year(year)
      year_data_by_key = {year:data_years}
      
      DisplayData().show_year_data(year, year_data_by_key)
      ```
      * The **Spent** class is used to extract the **spending data for the year**. And they are packaged in a dictionary.
    * ##### Display Month Data:
      ```python
      import os
      from budget_system import DisplayData, Spent
      
      base_folder = r"C:\Users\username\Documents\MyBudget"
  
      #If the environment variable for the configuration has not been set, we set it.
      if not os.environ.get('CONFIG_BUDGET'):
        os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')
  
      year, month = 2022, 'April'
      data_months = Spent().spending_by_month(year, month)
      month_data_by_key = {month : data_months}
      
      DisplayData().show_month_data(month, month_data_by_key)
      ```
      * The **Spent** class is used to extract the **spending data for the month**. And they are packaged in a dictionary.
    * ##### Display Store (sector) Data:
      ```python
      import os
      from budget_system import DisplayData, Spent
      from budget_system.settings.Config import ConfigBudget
      
      base_folder = r"C:\Users\username\Documents\MyBudget"
  
      #If the environment variable for the configuration has not been set, we set it.
      if not os.environ.get('CONFIG_BUDGET'):
        os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')
  
      year, month, store_name = 2022, 'April', 'StoreOne'
      month_path = ConfigBudget().MONTH_PATH.format(year=year, month=month)
      sector_data_by_key = Spent().spending_by_sector_in_month(month_path, store_name)[0]
      
      DisplayData().show_sector_data(store_name, sector_data_by_key)
      ```
      * The **Spent** class is used to extract the **spending data for the sector**. And they are packaged in a dictionary.
      * **_month_path_** refers to the folder where the **store's purchase data** tables are located, with one or more purchase dates in that month.
    * ##### Display Date (sector-date) Data:
      ```python
      import os
      from budget_system import DisplayData, Spent
      from budget_system.settings.Config import ConfigBudget
      
      base_folder = r"C:\Users\username\Documents\MyBudget"
  
      #If the environment variable for the configuration has not been set, we set it.
      if not os.environ.get('CONFIG_BUDGET'):
        os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')
  
      year, month, store_name, buy_date = 2022, 'April', 'StoreOne', '23-04-22'
      month_path = ConfigBudget().MONTH_PATH.format(year=year, month=month)
      sector_data_by_key = Spent().spending_by_sector_in_month(month_path, store_name)[0]
      date_data_by_key = {buy_date : sector_data_by_key[store_name][buy_date]}
      
      DisplayData().show_date_data(buy_date, date_data_by_key)
      ```
      * The **Spent** class is used to extract the **spending data for the sector**. And they are packaged in a dictionary.
      * **_month_path_** refers to the folder where the **store's purchase data** tables are located, with one or more purchase dates in that month.
## Data Processing
The main purpose of the package is to obtain and visualize spents, more expensive and less expensive products.

If you want to process table data directly, or spent and product data into dictionaries and tuples, or extract the date and name from a data table, **Budget System** has three classes: **_Spent_**, **_PurchaseList_** and **_ParserTableName_**.
### Spent
It follows a hierarchy of types, to pack the data in layers.
![Budget System Data Structure](https://raw.githubusercontent.com/carlosmperilla/budget-system/main/example%20imgs/budget_system_data_structure.png)
![Date Structure](https://raw.githubusercontent.com/carlosmperilla/budget-system/main/example%20imgs/budget_system_date_content.png)
It can be better understood by reviewing the types in **budget_system.extra_types.SpentTypes**
```python
ProductsData = NewType('ProductsData', Tuple[DataFrame, DataFrame, float64])
DatesDict = NewType('DatesDict', Dict[str, ProductsData])
SectorsDict = NewType('SectorsDict', Dict[str, DatesDict])
MonthData = NewType('MonthData', Tuple[SectorsDict, float64])
YearData = NewType('YearData',  Tuple[Dict[str, MonthData], float64])
TotalData = NewType('TotalData',  Tuple[Dict[int, YearData], float64])
```
##### ProductsData
The minimum data set, a tuple containing:
* Least expensive products.
* Most expensive products.
* Total spent of table (corresponding to a specific **date-store** or date-sector).

Being the **minimum data type** of **Spent**, it can be accessed from every main function. **There is no proper method in Spent** to extract this type of data.

Here we will use two approaches, the **concrete approach** (the function that extracts the minimum amount of data for the requested information). And the **full approach** (the function that extracts all the data and can look up a **ProductsData** among this data.)
* **Concrete**
  ```python
  import os
  from budget_system import Spent
  from budget_system.settings.Config import ConfigBudget
  
  base_folder = r"C:\Users\username\Documents\MyBudget"
  
  #If the environment variable for the configuration has not been set, we set it.
  if not os.environ.get('CONFIG_BUDGET'):
    os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')
 
  year, month, store_name, date = 2022, 'April', 'StoreOne', '23-04-22'
  d_index = 0 #dict index
  month_path = ConfigBudget().MONTH_PATH.format(year=year, month=month)
  products_data = Spent().spending_by_sector_in_month(month_path, store_name)[d_index][store_name][date]
  
  least_expensive, most_expensive, spent = products_data
  print(least_expensive)
  print(most_expensive)
  print(spent)
  ```
  * **spending_by_sector**: This returns the spent per store in a specific month, with information on each of its spending dates.
* **Full**
  ```python
  import os
  from budget_system import Spent
  
  base_folder = r"C:\Users\username\Documents\MyBudget"
  
  #If the environment variable for the configuration has not been set, we set it.
  if not os.environ.get('CONFIG_BUDGET'):
    os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')
 
  year, month, store_name, date = 2022, 'April', 'StoreOne', '23-04-22'
  d_index = 0 #dict index
  products_data = Spent().total_spending()[d_index][year][d_index][month][d_index][store_name][date]
  
  least_expensive, most_expensive, spent = products_data
  print(least_expensive)
  print(most_expensive)
  print(spent)
  ```
  * **total_spending:** This returns the total spent and inherited spent information.
##### DatesDict
Dictionary with **dates** as keys. And **ProductsData** as values.

**There is no proper method in Spent** to extract this type of data.

Here we will use two approaches, the **concrete approach** (the function that extracts the minimum amount of data for the requested information). And the **full approach** (the function that extracts all the data and can look up a **DatesDict** among this data.)
* **Concrete**
  ```python
  import os
  from budget_system import Spent
  from budget_system.settings.Config import ConfigBudget
  
  base_folder = r"C:\Users\username\Documents\MyBudget"
  
  #If the environment variable for the configuration has not been set, we set it.
  if not os.environ.get('CONFIG_BUDGET'):
    os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')
 
  year, month, store_name = 2022, 'April', 'StoreOne'
  d_index = 0 #dict index
  month_path = ConfigBudget().MONTH_PATH.format(year=year, month=month)
  dates_dict = Spent().spending_by_sector_in_month(month_path, store_name)[d_index][store_name]
  
  for date in dates_dict:
    print(f"Date of purchase: {date}")
    print(dates_dict[date], '\n')
  ```
  * **spending_by_sector**: This returns the spent per store in a specific month, with information on each of its spending dates.
* **Full**
  ```python
  import os
  from budget_system import Spent
  
  base_folder = r"C:\Users\username\Documents\MyBudget"
  
  #If the environment variable for the configuration has not been set, we set it.
  if not os.environ.get('CONFIG_BUDGET'):
    os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')
 
  year, month, store_name = 2022, 'April', 'StoreOne'
  d_index = 0 #dict index
  dates_dict = Spent().total_spending()[d_index][year][d_index][month][d_index][store_name]
  
  for date in dates_dict:
    print(f"Date of purchase: {date}")
    print(dates_dict[date], '\n')
  ```
  * **total_spending:** This returns the total spent and inherited spent information.
##### SectorsDict
Dictionary with **store names** as keys. And **DatesDict** as values.

**There is no proper method in Spent** to extract this type of data.

Here we will use two approaches, the **concrete approach** (the function that extracts the minimum amount of data for the requested information). And the **full approach** (the function that extracts all the data and can look up a **SectorsDict** among this data.)

If you want to know **the spent made in a store in a particular month**, check the section on **MonthData**.

* **Concrete**
  ```python
  import os
  from budget_system import Spent
  from budget_system.settings.Config import ConfigBudget
  
  base_folder = r"C:\Users\username\Documents\MyBudget"
  
  #If the environment variable for the configuration has not been set, we set it.
  if not os.environ.get('CONFIG_BUDGET'):
    os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')
 
  year, month, store_name = 2022, 'April'
  d_index = 0 #dict index
  month_path = ConfigBudget().MONTH_PATH.format(year=year, month=month)
  sectors_dict = Spent().spending_by_sector_in_month(month_path, store_name)[d_index]
  
  for sector in sectors_dict:
    print(f"Purchase dates in {sector} in {month}:")
    print(sectors_dict[sector], '\n')
  ```
  * **spending_by_sector**: This returns the spent per store in a specific month, with information on each of its spending dates.
* **Full**
  ```python
  import os
  from budget_system import Spent
  
  base_folder = r"C:\Users\username\Documents\MyBudget"
  
  #If the environment variable for the configuration has not been set, we set it.
  if not os.environ.get('CONFIG_BUDGET'):
    os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')
 
  year, month = 2022, 'April'
  d_index = 0 #dict index
  sectors_dict = Spent().total_spending()[d_index][year][d_index][month][d_index]
  
  for sector in sectors_dict:
    print(f"Purchase dates in {sector} in {month}:")
    print(sectors_dict[sector], '\n')
  ```
  * **total_spending:** This returns the total spent and inherited spent information.
##### MonthData
Tuple with **SectorsDict** and **the accumulated spent of these sectors**.

Being contained by months it is called **MonthData**, although it does not necessarily contain the information of the entire month, it can be that of only one store in that month.

Here we will use two approaches, the **exact approach** (the function that extracts the exact data for the requested information). And the **full approach** (the function that extracts all the data and can look up a **MonthData** among this data.)

There are two functions in **Spent** that allow us to get data of type **MonthData**. 

* **spending_by_month**: This returns the spent per month and inherited spent information.
* **spending_by_sector**: Like **spending_by_month** but only with **one store(sector)** the dictionaries of a specific store and the total spending of the store in that month.

How to extract spending and inherited information from **one month** to one year.
* **Exact**
  ```python
  import os
  from budget_system import Spent
  
  base_folder = r"C:\Users\username\Documents\MyBudget"
  
  #If the environment variable for the configuration has not been set, we set it.
  if not os.environ.get('CONFIG_BUDGET'):
    os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')
 
  year, month = 2022, 'April'
  month_data = Spent().spending_by_month(year, month)
  
  month_content, month_spent = month_data 
  
  print(f"Spent in {month}:", month_spent)
  print(f"Data on store spents in the month:")
  print(month_content)
  ```
* **Full**
  ```python
  import os
  from budget_system import Spent
  
  base_folder = r"C:\Users\username\Documents\MyBudget"
  
  #If the environment variable for the configuration has not been set, we set it.
  if not os.environ.get('CONFIG_BUDGET'):
    os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')
 
  year, month = 2022, 'April'
  d_index = 0 #dict index
  month_data = Spent().total_spending()[d_index][year][d_index][month]
  
  month_content, month_spent = month_data 
  
  print(f"Spent in {month}:", month_spent)
  print(f"Data on store spents in the month:")
  print(month_content)
  ```
How to extract spending and inherited information from **one store in a month**, in a year. Here we can only apply the **exact approach** by the intrinsic structure in **TotalData**.
* **Exact**
  ```python
  import os
  from budget_system import Spent
  from budget_system.settings.Config import ConfigBudget
  
  base_folder = r"C:\Users\username\Documents\MyBudget"
  
  #If the environment variable for the configuration has not been set, we set it.
  if not os.environ.get('CONFIG_BUDGET'):
    os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')
 
  year, month, store_name = 2022, 'April', 'StoreOne'
  month_path = ConfigBudget().MONTH_PATH.format(year=year, month=month)
  month_data = Spent().spending_by_sector_in_month(month_path, store_name)
  
  month_content, month_spent = month_data 
  
  print(f"Spent in {store_name} in {month}:", month_spent)
  print(f"Data on store spent in the month:")
  print(month_content)
  ```
##### YearData
Tuple with a dictionary with **months** as keys and **MonthData**  as value. And **the accumulated spent of these months**.

Here we will use two approaches, the **exact approach** (the function that extracts the exact data for the requested information). And the **full approach** (the function that extracts all the data and can look up a **YearData** among this data.)

How to extract spending and inherited information from **one year**.
* **Exact**
  ```python
  import os
  from budget_system import Spent
  
  base_folder = r"C:\Users\username\Documents\MyBudget"
  
  #If the environment variable for the configuration has not been set, we set it.
  if not os.environ.get('CONFIG_BUDGET'):
    os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')
 
  year = 2022
  year_data = Spent().spending_by_year(year)
  
  year_content, year_spent = year_data 
  
  print(f"Spent in {year}:", year_spent)
  print(f"Data on month spents in the year:")
  print(year_content)
  ```
* **Full**
  ```python
  import os
  from budget_system import Spent
  
  base_folder = r"C:\Users\username\Documents\MyBudget"
  
  #If the environment variable for the configuration has not been set, we set it.
  if not os.environ.get('CONFIG_BUDGET'):
    os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')
 
  year = 2022
  d_index = 0 #dict index
  year_data = Spent().total_spending()[d_index][year]
  
  year_content, year_spent = year_data 
  
  print(f"Spent in {year}:", year_spent)
  print(f"Data on month spents in the year:")
  print(year_content)
  ```
##### TotalData
Tuple with a dictionary with **years** as keys and **YearData** as value. And **the accumulated spent of these years**.

Being the structure with the highest hierarchy, the **exact** and **full** approach are **the same**.

```python
import os
from budget_system import Spent

base_folder = r"C:\Users\username\Documents\MyBudget"

#If the environment variable for the configuration has not been set, we set it.
if not os.environ.get('CONFIG_BUDGET'):
  os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')

total_data = Spent().total_spending()

total_content, total_spent = total_data 

print(f"Total Spent:", total_spent)
print(f"Total Data in Budget System:")
print(total_content)
```
### PurchaseList
Class that reads the table with the **purchases**, sorts them by price and extracts the **relevant data**.

If we want more specific data from a specific table (remembering that each table is a purchase date in a store). PurchaseList can be useful.

How to get the **ProductsData** directly from the table. Let's remember that the minimum type that directly returns **Spent** is **MonthData**.

The maximum type that this class returns is **ProductsData**.
```python
import os
from budget_system import PurchaseList
from budget_system.settings.Config import ConfigBudget

base_folder = r"C:\Users\username\Documents\MyBudget"

#If the environment variable for the configuration has not been set, we set it.
if not os.environ.get('CONFIG_BUDGET'):
  os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')

year, month = 2022, 'April'
month_path = ConfigBudget().MONTH_PATH.format(year=year, month=month)
file_name = 'Purchase_List_StoreOne_[23-04-22].csv'

location = os.path.join(month_path, file_name)

products_data = PurchaseList(location).get_all()

least_expensive, most_expensive, spent = products_data
print(least_expensive)
print(most_expensive)
print(spent)
```
How to get the **n most expensive products**. By default **n = 3**.
```python
import os
from budget_system import PurchaseList
from budget_system.settings.Config import ConfigBudget

base_folder = r"C:\Users\username\Documents\MyBudget"

#If the environment variable for the configuration has not been set, we set it.
if not os.environ.get('CONFIG_BUDGET'):
  os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')

year, month = 2022, 'April'
month_path = ConfigBudget().MONTH_PATH.format(year=year, month=month)
file_name = 'Purchase_List_StoreOne_[23-04-22].csv'

location = os.path.join(month_path, file_name)

n_products = 5
most_expensive = PurchaseList(location).most_expensive(n_products)

print(most_expensive)
```
How to get the **n least expensive products**. By default **n = 3**.
```python
import os
from budget_system import PurchaseList
from budget_system.settings.Config import ConfigBudget

base_folder = r"C:\Users\username\Documents\MyBudget"

#If the environment variable for the configuration has not been set, we set it.
if not os.environ.get('CONFIG_BUDGET'):
  os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')

year, month = 2022, 'April'
month_path = ConfigBudget().MONTH_PATH.format(year=year, month=month)
file_name = 'Purchase_List_StoreOne_[23-04-22].csv'

location = os.path.join(month_path, file_name)

n_products = 5
least_expensive = PurchaseList(location).least_expensive(n_products)

print(least_expensive)
```
How to get the **total spent**.
```python
import os
from budget_system import PurchaseList
from budget_system.settings.Config import ConfigBudget

base_folder = r"C:\Users\username\Documents\MyBudget"

#If the environment variable for the configuration has not been set, we set it.
if not os.environ.get('CONFIG_BUDGET'):
  os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')

year, month = 2022, 'April'
month_path = ConfigBudget().MONTH_PATH.format(year=year, month=month)
file_name = 'Purchase_List_StoreOne_[23-04-22].csv'

location = os.path.join(month_path, file_name)

spent_by_table = PurchaseList(location).spending_by_sector()

print(f"{file_name} records an spent of:")
print(spent_by_table)
```
How to access the **full dataframe**.
```python
import os
from budget_system import PurchaseList
from budget_system.settings.Config import ConfigBudget

base_folder = r"C:\Users\username\Documents\MyBudget"

#If the environment variable for the configuration has not been set, we set it.
if not os.environ.get('CONFIG_BUDGET'):
  os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')

year, month = 2022, 'April'
month_path = ConfigBudget().MONTH_PATH.format(year=year, month=month)
file_name = 'Purchase_List_StoreOne_[23-04-22].csv'

location = os.path.join(month_path, file_name)

df = PurchaseList(location).data_frame

print(df)
```
How to access the **full dataframe** sortered by the **price column**.
```python
import os
from budget_system import PurchaseList
from budget_system.settings.Config import ConfigBudget

base_folder = r"C:\Users\username\Documents\MyBudget"

#If the environment variable for the configuration has not been set, we set it.
if not os.environ.get('CONFIG_BUDGET'):
  os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')

year, month = 2022, 'April'
month_path = ConfigBudget().MONTH_PATH.format(year=year, month=month)
file_name = 'Purchase_List_StoreOne_[23-04-22].csv'

location = os.path.join(month_path, file_name)

df_by_price = PurchaseList(location).df_by_price

print(df_by_price)
```
### ParserTableName
Class to **parse and extract** data from **table name**.

This is one of the few classes that **does not require the CONFIG_BUDGET** environment variable to be set **to work**.

How to extract the **name of the store**.
```python
from budget_system import ParserTableName

file_name = 'Purchase_List_StoreOne_[23-04-22].csv'

store_name = ParserTableName(file_name).get_store_name()

print(store_name) #'StoreOne'
```
How to extract the date of purchase.
```python
from budget_system import ParserTableName

file_name = 'Purchase_List_StoreOne_[23-04-22].csv'

table_date = ParserTableName(file_name).get_table_date()

print(table_date) #'23-04-22'
```
How to get the **name of the store** and the **date of purchase**.
```python
from budget_system import ParserTableName

file_name = 'Purchase_List_StoreOne_[23-04-22].csv'

store_name, table_date = ParserTableName(file_name).get_all()

print(f"File: {file_name}")
print(f"Name of the store: {store_name}")
print(f"Table date: {table_date}")
```
## Translation
The package has two languages integrated by default, **English (ENG)** and **Spanish (SPA)**.

This is mainly used for **the months** in the **Budget System** folder tree, **display messages** and **error messages**.

As the text used is very little, the package has two specialized classes to facilitate the integration of **new languages** to the package for **your personal use**.

Specifically:
* You can **add new languages**.
* **Add and translate** in one step.
* **Translate to available languages** (either by default or added for future uses).

I **recommend** creating the Budget System in **English or Spanish** and translating it later, if necessary. For compatibility issues.

### Only translation

Suppose that your operating system is configured by default in Spanish, and you did not explicitly specify that the **Budget System** be in English. But you need it in English. For this case you **only need a translation**.

For this we use the **_translate_month_folders_** method of the **Budget** class.
```python
import os
from budget_system import Budget
from budget_system.settings.Config import ConfigBudget

base_folder = r"C:\Users\username\Documents\MyBudget"

#If the environment variable for the configuration has not been set, we set it.
if not os.environ.get('CONFIG_BUDGET'):
  os.environ['CONFIG_BUDGET'] = os.path.join(base_folder, 'config.ini')

config_path = ConfigBudget().CONFIG_FILE_PATH
Budget.translate_month_folders(config_path, 'SPA', 'ENG')
```
   
 * As you can see, you can also use the **CONFIG_BUDGET** environment variable to get the configuration file directory, instead of using the **ConfigBudget** class.
 * First the **current language** is passed, and then the one you want to translate to.
 * It can be translated into languages **other than Spanish or English**, if these have been **previously added**, to learn **how to add a new language** read later.
 * The **_translate_month_folders_** function not only translates the directories, it also **changes the language in the configuration file**.
### Add a new language
You can add the language through **a file** with the translated text strings or with **a dictionary**.

#### By File
The recommended and most practical method is through **a file**. You just translate the following text (which we will call **_main_lang_text.txt_**) and save it to a **text file**.
```
January, February, March, April, May, June, July, August, September, October, November, December
message_monthnotvalid = The month entered is not valid.
message_monthempty = Missing to assign a month for the search.
message_totalspent = Total Spent
message_yearspent = Expenses made in {year}
message_monthspent = Expenses made in {month}
message_datespent = Spent
message_leastexpensive = Products with less cost
message_mostexpensive = Products with greater cost
message_foldertreedoesntexist = The required folder tree has not been created.
message_invalidconfigfile = An environment valid variable has not been assigned for config.
message_unallocatedconfigfile = Missing setting environment variable CONFIG_BUDGET with path of config.ini
```
* The **first line** corresponds to the **months**. They must be **separated by commas** and **ordered**.
* The **text to the left** of the equal must remain **intact**, it corresponds to the **variables used for the messages**.
* **{year}** and **{month}** are variables. therefore they should not be translated or modified in any way.
* **CONFIG_BUDGET**, **config.ini** must remain the same, to make sense.

To add the language we would use the **FileToLangContext** class and its **_add_new_lang_** method.
```python
from budget_system import FileToLangContext
# from budget_system.settings.config import ConfigBudget

new_lang_file = f"C:\Users\username\Documents\portuguese_lang_text.txt"
lang_key_name = "POR"
file_to = FileToLangContext(new_lang_file)
file_to.add_new_lang(lang_key_name)

# config_path = ConfigBudget().CONFIG_FILE_PATH
# Budget.translate_month_folders(config_path, 'ENG', 'POR')
```
* **portuguese_lang_text.txt** would be the translation of **main_lang_text.txt**, taking into account all the previous indications.
* As a standard, it is recommended to use the first three uppercase letters of the language name in English as the key name of the language. For example for Portuguese we use **"POR"**.
* If we define the environment variable **CONFIG_BUDGET** and uncomment the lines, in addition to adding, it would be **translated from English to Portuguese**.
#### By Dictionary
To add the language **without file** we would use the **SupportLanguage** class and its **_add_new_lang_** method.
```python
from budget_system import SupportLanguage

new_lang = "GER"
months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
sections = {
    "Month" : {
        "message_MonthNotValid": "Der eingegebene Monat ist ungültig.",
        "message_MonthEmpty": "Zuweisung des Monats für die Suche fehlt."
    },
    "ShowData" : {
        "message_TotalSpent": "Gesamtausgaben",
        "message_YearSpent": "Ausgegeben in {year}",
        "message_MonthSpent": "Ausgegeben in {month}",
        "message_DateSpent": "Verbracht",
        "message_LeastExpensive": "Produkte zu einem niedrigeren Preis",
        "message_MostExpensive": "Produkte mit höheren Kosten"
    },
    "BudgetSystem" : {
        "message_FolderTreeDoesntExist" : "Der erforderliche Ordnerbaum wurde nicht erstellt."
    },
    "Settings" : {
        "message_InvalidConfigFile": "Für die Konfiguration wurde keine gültige Umgebungsvariable zugewiesen.",
        "message_UnallocatedConfigFile": "Fehlende CONFIG_BUDGET Tuning-Umgebungsvariable mit Pfad zu config.ini"
    }
}

translation_system = SupportLanguage(
                                    new_lang=new_lang,
                                    months=months,
                                    sections=sections
                                    )

translation_system.add_new_lang()
```
### Add a new language and Translate
You can add and translate the language through **a file** with the translated text strings or with **a dictionary**.

#### By File
The recommended and most practical method is through **a file**. You just translate the following text (which we will call **_main_lang_text.txt_**) and save it to a **text file**.
```
January, February, March, April, May, June, July, August, September, October, November, December
message_monthnotvalid = The month entered is not valid.
message_monthempty = Missing to assign a month for the search.
message_totalspent = Total Spent
message_yearspent = Expenses made in {year}
message_monthspent = Expenses made in {month}
message_datespent = Spent
message_leastexpensive = Products with less cost
message_mostexpensive = Products with greater cost
message_foldertreedoesntexist = The required folder tree has not been created.
message_invalidconfigfile = An environment valid variable has not been assigned for config.
message_unallocatedconfigfile = Missing setting environment variable CONFIG_BUDGET with path of config.ini
```
* The **first line** corresponds to the **months**. They must be **separated by commas** and **ordered**.
* The **text to the left** of the equal must remain **intact**, it corresponds to the **variables used for the messages**.
* **{year}** and **{month}** are variables. therefore they should not be translated or modified in any way.
* **CONFIG_BUDGET**, **config.ini** must remain the same, to make sense.

To add and translate the language we would use the **FileToLangContext** class and its **_translate_to_new_lang_** method.
```python
from budget_system import FileToLangContext
from budget_system.settings.config import ConfigBudget

new_lang_file = f"C:\Users\username\Documents\portuguese_lang_text.txt"
lang_key_name = "POR"
current_lang = "ENG"
config_path = ConfigBudget().CONFIG_FILE_PATH

file_to = FileToLangContext(new_lang_file)
file_to.translate_to_new_lang(
                new_lang=lang_key_name,
                config_file_path=config_path,
                current_lang=current_lang
                )
```
* **portuguese_lang_text.txt** would be the translation of **main_lang_text.txt**, taking into account all the previous indications.
* As a standard, it is recommended to use the first three uppercase letters of the language name in English as the key name of the language. For example for Portuguese we use **"POR"**.
* Note that we **don't need** to use the **Budget** class to translate.
#### By Dictionary
To add the language and translate **without file** we would use the **SupportLanguage** class and its **_translate_to_new_lang_** method.
```python
from budget_system import SupportLanguage
from budget_system.settings.config import ConfigBudget

new_lang = "GER"
months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
sections = {
    "Month" : {
        "message_MonthNotValid": "Der eingegebene Monat ist ungültig.",
        "message_MonthEmpty": "Zuweisung des Monats für die Suche fehlt."
    },
    "ShowData" : {
        "message_TotalSpent": "Gesamtausgaben",
        "message_YearSpent": "Ausgegeben in {year}",
        "message_MonthSpent": "Ausgegeben in {month}",
        "message_DateSpent": "Verbracht",
        "message_LeastExpensive": "Produkte zu einem niedrigeren Preis",
        "message_MostExpensive": "Produkte mit höheren Kosten"
    },
    "BudgetSystem" : {
        "message_FolderTreeDoesntExist" : "Der erforderliche Ordnerbaum wurde nicht erstellt."
    },
    "Settings" : {
        "message_InvalidConfigFile": "Für die Konfiguration wurde keine gültige Umgebungsvariable zugewiesen.",
        "message_UnallocatedConfigFile": "Fehlende CONFIG_BUDGET Tuning-Umgebungsvariable mit Pfad zu config.ini"
    }
}

config_file_path = ConfigBudget().CONFIG_FILE_PATH
current_lang = "ENG"

translation_system = SupportLanguage(
                                    new_lang=new_lang,
                                    months=months,
                                    sections=sections,
                                    config_file_path=config_file_path,
                                    current_lang=current_lang
                                    )

translation_system.translate_to_new_lang()
```
* For the translation you need in addition to what is required to add the language, the **current language** of the **Budget System** and the **location of its configuration file**. These parameters are mandatory.

## License

MIT License

Copyright (c) 2022 Carlos Perilla Budget System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


[pandas install]: https://pypi.org/project/pandas/
[colorama install]: https://pypi.org/project/colorama/
[numpy install]: https://pypi.org/project/numpy/
[date format python]: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes