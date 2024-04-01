# PetFinder Historical Dashboard

The goal of this project was to analyze trends in adoptable dogs in the United States.

Initially, I had hoped to utilize the PetFinder API. However, upon reaching out to obtain an API key, I was informed by customer service that the API is currently closed to new applications. This was disappointing, but  I was able to locate historical data from 09/20/2019. <sub>Thank you Amber Thomas.</sub>

The main caveat to note when viewing this project is that the data being used is from a single day only and is several years out of date. I have done my best to emulate the kinds of analysis I was planning on doing if I had been able to get access to the API and had more freedom to query by time.


# Tools

 - **Languages Used:** Python (Pandas, PyArrow)
 -  **Infrastructure as Code**: Terraform
 - **Data Orchestration:** Mage
 - **Data Transformation:** Mage
 - **Data Lake:** Google Cloud Storage
 - **Data Warehouse:** BigQuery
 - **Data Visualization:** Looker Studio

![Pipeline Flowchart](https://github.com/itssnowing/dog-adoption-simple-data-analysis/blob/main/images/pipeline-flowchart.png?raw=true)

## Dataset Used

As mentioned, this is a historical dataset of PetFinder API information gathered from a single day - 09/20/2019 as the API is no longer accepting new applications.
[Adoptable Dogs on PetFinder in the US](https://data.world/the-pudding/adoptable-dogs-on-petfinder-in-the-us)

# Reproduction

These steps assume you already have a Google Cloud Platform profile and Mage is installed either [locally](https://docs.mage.ai/getting-started/setup) or [in Cloud Run](https://docs.mage.ai/production/deploying-to-cloud/gcp/setup). The project can be ran entirely within the Google Cloud Platform and uses no other external tools.

### Terraform

 - Create a new folder for this project anywhere on your machine
	 - For the instructions the following path will be referenced:
	 - `./petfinder-project/`
 - Create a new folder in the project directory to host your Google Cloud Service Account Credentials
	 - `./petfinder-project/keys/`
	 - Add your keys.json file to the above directory
		 - Google IAM Roles needed:
			 - Storage Admin
			 - Storage Object Admin
			 - BigQuery Admin
- Create a sub-folder for Terraform in the project directory
	- `./petfinder-project/terraform/`
	- Copy main.tf and variables.tf from the terraform folder in this repo into the terraform folder
	- cd into your terraform folder via your terminal
	- Run the following commands:
    ```
    terraform init
    terraform plan
    terraform apply
    ```

### Mage
Mage was utilized to extract, transform, and load data in one place using a batch operation. This project did not require the transformation capabilities of dbt or pySpark. The transformations are done entirely in Mage using Pandas.
 - Create a fresh pipeline for the project
 - Download the files in the mage folder in this repo
 - Import the files directly or copy & paste them into the appropriate tool types
	 - **data_loaders:** *get_petfinder_data.py*
	 - **transformers:** *clean_petfinder_data.py*
	 - **data_exporters:**
		 - *export_petfinder_to_gcs.py* **UPDATE THE BUCKET NAME**
		 - *export_petfinder_to_bq.py* **UPDATE THE PROJECT ID**
 - Set your tree to look like this:

![Mage Project Tree](https://github.com/itssnowing/dog-adoption-simple-data-analysis/blob/main/images/mage-tree.PNG?raw=true)

Note - If you are running Mage in Cloud Run and are struggling to get your keys.json file into Mage, then follow these steps:

 - Download your keys.json file for your Mage Service Account in GCP > IAM > Service Accounts > Keys
 - In Mage, right-click default_repo > Upload files > drag & drop keys.json
 - The default Mage folder structure path is /home/src/default_repo
 - Edit io_config.yaml and set GOOGLE_SERVICE_ACC_KEY_FILEPATH to your keys.json location
	 - Should be /home/src/default_repo/keys.json if you dropped it directly without moving it
 - Comment out or delete everything below & including GOOGLE_SERVICE_ACC_KEY
	 - Do not delete or comment out GOOGLE_SERVICE_ACC_KEY_FILEPATH
 - Save

## Result

I created a dashboard using Google Looker Studio. As mentioned, all transformations were done in Mage. No further transformations or partitioning were done using BigQuery - in tests, partitioning the data actually lowered performance.

You can view the dashboard here:
[PetFinder Dog Statistics](https://lookerstudio.google.com/s/jHoR_VSwOqw)


