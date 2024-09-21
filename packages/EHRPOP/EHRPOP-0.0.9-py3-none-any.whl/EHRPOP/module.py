import numpy as np
import plotly.graph_objects as go
import pandas as pd
import re
import json
from datetime import date

data = dict()

def read_traitements_data(json_path):
    """
    Reads treatment data from a JSON file and returns the corresponding dictionary.

    Parameters
    ----------
    json_path : str
        The path to the JSON file containing treatment data.

    Returns
    -------
    dict
        A dictionary containing the treatment data from the JSON file.
    """

    global data
    # Load the JSON data
    with open(json_path, 'r') as file:
        data = json.load(file)
    

def find_code(code):
    """
    Finds the location of a code within the Treatment structure.
    
    :param code: The code to search for.
    :return: A message indicating the treatment type and code type, or a not found message.
    """
    if "Treatment" in data and isinstance(data["Treatment"], dict):
        for treatment_type, treatment_data in data['Treatment'].items():
            # Check if the treatment_data is a dictionary (with code types like 'CCAM', 'ICD10', etc.)
            if isinstance(treatment_data, dict):
                for _, code_list in treatment_data.items():
                    if isinstance(code_list, list) and code in code_list:
                        return treatment_type
    
    return np.nan


def sankey_diagram(df, index_date="DATE", index_code_ccam="CODE_CCAM", 
                   index_code_atc="CODE_ATC", index_code_icd="CODE_ICD10", 
                   index_id="ID_PATIENT"):
    """
    Generates and displays a Sankey diagram visualizing patient treatment sequences based on medical records.

    The Sankey diagram provides a graphical representation of the flow of treatment sequences for patients,
    allowing for the visualization of how different treatment codes (CCAM, ATC, ICD10) are distributed and
    transitioned over time.

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records. It should include the following columns:
        - ID_PATIENT: Unique identifier for each patient.
        - DATE: Date of the treatment or medical record entry.
        - CODE_CCAM: CCAM codes representing specific medical acts or treatments.
        - CODE_ATC: ATC codes representing medication classes.
        - CODE_ICD10: ICD10 codes representing diagnoses.

    index_date : str, optional
        The column name in df representing the date of the treatment (default is "DATE").
    index_code_ccam : str, optional
        The column name in df representing CCAM codes (default is "CODE_CCAM").
    index_code_atc : str, optional
        The column name in df representing ATC codes (default is "CODE_ATC").
    index_code_icd : str, optional
        The column name in df representing ICD10 codes (default is "CODE_ICD10").
    index_id : str, optional
        The column name in df representing patient IDs (default is "ID_PATIENT").

    Returns
    -------
    None
        This function processes the DataFrame and displays a Sankey diagram. The Sankey diagram visualizes the flow of
        treatments for each patient, showing how treatments transition over time. The diagram helps in understanding
        the distribution and sequence of different medical treatments.

    Notes
    -----
    Ensure that the DataFrame `df` is properly preprocessed and contains all required columns with appropriate data
    before calling this function. The function uses Plotly to generate and display the Sankey diagram.
    """


    # Check if the 'data' dictionary contains 'Treatment' key
    if data is None or 'Treatment' not in data:
        raise ValueError("Treatment data must be read and processed before generating the Sankey diagram.")
    

    df['CODE_ACT'] = df[index_code_ccam].combine_first(df[index_code_atc]).combine_first(df[index_code_icd])

    df = df.drop(columns=[index_code_icd, index_code_ccam,index_code_atc])

    df = df.dropna(subset=['CODE_ACT'])
    
    # Apply the function to CODE_ACT column
    df['CODE_ACT'] = df['CODE_ACT'].apply(find_code)

    df = df.dropna(subset=['CODE_ACT'])

    df = df.sort_values(by=index_date, ascending=True)
    
    df[index_date] = pd.to_numeric(df[index_date], errors='coerce').fillna(999999)

    # Sort the DataFrame by ID_PATIENT and DATE
    df = df.sort_values(by=[index_id, index_date])
    
    def remove_consecutive_duplicates(treatments):
        return '->'.join([treatments[i] for i in range(len(treatments)) if i == 0 or treatments[i] != treatments[i-1]])

    # Group by ID_PATIENT and concatenate the CODE_ACT values without consecutive duplicates
    result = df.groupby(index_id)['CODE_ACT'].apply(lambda x: remove_consecutive_duplicates(list(x))).reset_index()

    result.columns = [index_id, 'Traitements']
        
    treatment_counts = result['Traitements'].value_counts()
        
    # Filter out sequences that appear fewer than 10 times
    frequent_treatments = treatment_counts[treatment_counts >= 10].index

    # Filter the original DataFrame to keep only the frequent treatment sequences
    filtered_df = result[result['Traitements'].isin(frequent_treatments)]

    # Function to split treatments and label them uniquely
    def label_treatments(treatment_string):
        treatments = treatment_string.split('->')
        labeled_treatments = [f"{treatments[i]}{i+1}" for i in range(len(treatments))]
        return labeled_treatments
    
    sequence_counter = {}

    for treatments in filtered_df['Traitements']:
        sequence_list = label_treatments(treatments)
        for i in range(len(sequence_list) - 1):
            pair = (sequence_list[i], sequence_list[i + 1])
            if pair in sequence_counter:
                sequence_counter[pair] += 1
            else:
                sequence_counter[pair] = 1
                
    
    # Create source and target lists and values
    source = []
    target = []
    value = []

    for (src, tgt), val in sequence_counter.items():
        source.append(src)
        target.append(tgt)
        value.append(val)

    # Create a list of unique nodes
    all_nodes = list(set(source + target))
    
    node_indices = {node: idx for idx, node in enumerate(all_nodes)}

    # Map source and target to their indices
    source_indices = [node_indices[src] for src in source]
    target_indices = [node_indices[tgt] for tgt in target]
    
    # Create Sankey diagram
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_nodes,
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=value,
        )
    ))

    # Add annotations for the legend
    fig.update_layout(
        title_text="Sankey Diagram of Patient Treatment Sequences",
        font_size=10,
        margin=dict(l=50, r=200, t=50, b=50)  # Add margin on the right for the legend
    )
    fig.show()


def starts_with_any(code, codes_list):
    if pd.isnull(code): 
        return False
    return any(code.startswith(prefix) for prefix in codes_list)

def yes_or_no(df, CCAM_codes, ATC_codes, ICD_Codes, column_name, days_before, days_after, 
              index_date="DATE", index_code_ccam="CODE_CCAM", index_code_atc="CODE_ATC", 
              index_code_icd="CODE_ICD10", index_id="ID_PATIENT", bc_index_surgery="BC_index_surgery"):
    '''
    Evaluates whether patients have received treatments encoded by CCAM, ATC, or ICD codes within a specified timeframe relative to their breast cancer surgery date. Outputs a DataFrame indicating whether each patient meets the specified criteria.

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records, including columns for patient ID (ID_PATIENT), treatment codes (CODE_CCAM, CODE_ATC, CODE_ICD10), and treatment dates (DATE).
    CCAM_codes : list
        A list of CCAM codes. The function checks whether patients have received treatments coded with any of these CCAM codes.
    ATC_codes : list
        A list of ATC codes. Similar to CCAM_codes, this parameter specifies the ATC codes of interest for identifying relevant treatments.
    ICD_Codes : list
        A list of ICD codes used to identify relevant treatments based on these codes.
    column_name : str
        A string specifying the name of the output column in the result DataFrame that indicates whether each patient meets the criteria. This column will contain boolean values (True/False).
    days_before : int
        An integer specifying the number of days before breast cancer surgery within which treatments are considered relevant.
    days_after : int
        An integer specifying the number of days after breast cancer surgery within which treatments are considered relevant.
    index_date : str, optional
        The column name for treatment dates in df (default is "DATE").
    index_code_ccam : str, optional
        The column name for CCAM codes in df (default is "CODE_CCAM").
    index_code_atc : str, optional
        The column name for ATC codes in df (default is "CODE_ATC").
    index_code_icd : str, optional
        The column name for ICD codes in df (default is "CODE_ICD10").
    index_id : str, optional
        The column name for patient ID in df (default is "ID_PATIENT").
    bc_index_surgery : str, optional
        The column name for breast cancer surgery dates in df (default is "BC_index_surgery").

    Returns
    -------
    DataFrame
        A DataFrame indicating, for each patient, whether they meet the specified criteria with a boolean value in the column specified by columnName.
    '''
    
    df['DATE_DIFF'] = df[index_date] - df[bc_index_surgery]

    matches = ((df[index_code_ccam].isin(CCAM_codes) |
           df[index_code_atc].isin(ATC_codes) |
           df[index_code_icd].isin(ICD_Codes))& (df['DATE_DIFF'] >= -days_before) & (df['DATE_DIFF'] <= days_after) )
    
    result = matches.groupby(df[index_id]).any().reset_index()
    
    result = result.rename(columns={0: column_name})

    return result




def is_treated_by_it(df, CCAM_codes, ATC_codes, ICD_Codes, column_name,
                     index_code_ccam="CODE_CCAM", index_code_atc="CODE_ATC",
                     index_code_icd="CODE_ICD10", index_id="ID_PATIENT"):
    '''
    Assesses treatment records in a DataFrame to determine if each patient has received a treatment corresponding to any of the provided CCAM, ATC, or ICD codes. Generates a summary DataFrame that includes each patient's ID and a boolean indicator of whether they have received any of the specified treatments.

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records. This DataFrame should include columns for patient ID (ID_PATIENT), treatment codes (CODE_CCAM, CODE_ATC, CODE_ICD10), and treatment dates (DATE). It also includes an alternate date column (DATE_ENTREE) for use when the DATE is missing.
    CCAM_codes : list
        A list of CCAM codes used to identify relevant treatments.
    ATC_codes : list
        A list of ATC codes used to identify relevant treatments.
    ICD_Codes : list
        A list of ICD codes used to identify relevant treatments.
    column_name : str
        A string specifying the name for the output column in the resulting DataFrame. This column will contain boolean values indicating whether each patient has received any treatment matching the specified codes.
    index_code_ccam : str, optional
        The column name for CCAM codes in df (default is "CODE_CCAM").
    index_code_atc : str, optional
        The column name for ATC codes in df (default is "CODE_ATC").
    index_code_icd : str, optional
        The column name for ICD codes in df (default is "CODE_ICD10").
    index_id : str, optional
        The column name for patient ID in df (default is "ID_PATIENT").

    Returns
    -------
    DataFrame
        A DataFrame indicating, for each patient, whether they have received any treatment matching the specified codes with a boolean value in the column specified by columnName.
    '''

    matches = (df[index_code_ccam].isin(CCAM_codes) |
           df[index_code_atc].isin(ATC_codes) |
           df[index_code_icd].isin(ICD_Codes))
    
    result = matches.groupby(df[index_id]).any().reset_index()
    
    result = result.rename(columns={0: column_name})

    return result



def is_treated_by_it_percentage(df, CCAM_codes, ATC_codes, ICD_Codes, 
                                index_code_ccam="CODE_CCAM", index_code_atc="CODE_ATC", 
                                index_code_icd="CODE_ICD10", index_id="ID_PATIENT"):
    '''
    Determines the number and percentage of patients treated by the specified CCAM, ATC, or ICD codes.
    
    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    CCAM_codes : list
        A list of CCAM codes used to identify relevant treatments.
    ATC_codes : list
        A list of ATC codes used to identify relevant treatments.
    ICD_Codes : list
        A list of ICD codes used to identify relevant treatments.
    index_code_ccam : str, optional
        The column name for CCAM codes in df (default is "CODE_CCAM").
    index_code_atc : str, optional
        The column name for ATC codes in df (default is "CODE_ATC").
    index_code_icd : str, optional
        The column name for ICD codes in df (default is "CODE_ICD10").
    index_id : str, optional
        The column name for patient ID in df (default is "ID_PATIENT").

    Returns
    -------
    tuple
        A tuple containing:
        - The number of patients treated with any of the specified codes.
        - The percentage of patients treated relative to the total number of patients.
    '''
    
    # Create a mask for the rows that match any of the codes
    matches = (df[index_code_ccam].isin(CCAM_codes) |
               df[index_code_atc].isin(ATC_codes) |
               df[index_code_icd].isin(ICD_Codes))
    
    # Get the unique patient IDs that have a matching treatment
    treated_patients = df.loc[matches, index_id].nunique()
    
    # Get the total number of unique patients
    total_patients = df[index_id].nunique()
    
    # Calculate the percentage of treated patients
    treated_percentage = (treated_patients / total_patients) * 100
    
    return ""+str(treated_patients)+" (" +str(treated_percentage)+"%)"



def is_treated_by_it_with_date(df, CCAM_codes, ATC_codes, ICD_Codes, column_name, 
                               days_before, days_after, index_date="DATE", 
                               index_code_ccam="CODE_CCAM", index_code_atc="CODE_ATC", 
                               index_code_icd="CODE_ICD10", index_id="ID_PATIENT", 
                               bc_index_surgery="BC_index_surgery"):
    '''
    Assesses treatment records in a DataFrame to determine if each patient has received a treatment corresponding to any of the provided CCAM, ATC, or ICD codes within a specified timeframe relative to their breast cancer surgery date. Generates a summary DataFrame that includes each patient's ID, a boolean indicator of whether they have received any of the specified treatments, and the date of the first treatment.

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records. This DataFrame should include columns for patient ID (ID_PATIENT), treatment codes (CODE_CCAM, CODE_ATC, CODE_ICD10), and treatment dates (DATE). It also includes an alternate date column (DATE_ENTREE) for use when the DATE is missing.
    CCAM_codes : list
        A list of CCAM codes used to identify relevant treatments.
    ATC_codes : list
        A list of ATC codes used to identify relevant treatments.
    ICD_Codes : list
        A list of ICD codes used to identify relevant treatments.
    column_name : str
        A string specifying the name for the output column in the resulting DataFrame. This column will contain boolean values indicating whether each patient has received any treatment matching the specified codes.
    days_before : int
        The number of days before surgery within which treatments are considered relevant.
    days_after : int
        The number of days after surgery within which treatments are considered relevant.
    index_date : str, optional
        The column name for treatment dates in df (default is "DATE").
    index_code_ccam : str, optional
        The column name for CCAM codes in df (default is "CODE_CCAM").
    index_code_atc : str, optional
        The column name for ATC codes in df (default is "CODE_ATC").
    index_code_icd : str, optional
        The column name for ICD codes in df (default is "CODE_ICD10").
    index_id : str, optional
        The column name for patient ID in df (default is "ID_PATIENT").
    bc_index_surgery : str, optional
        The column name for the breast cancer surgery date in df (default is "BC_index_surgery").

    Returns
    -------
    DataFrame
        A DataFrame indicating, for each patient, whether they have received any treatment matching the specified codes with a boolean value in the column specified by columnName, and the date of the first such treatment.
    '''

    df['DATE_DIFF'] = df[index_date] - df[bc_index_surgery]
    
    df = df[(df['DATE_DIFF'] >= -days_before) & (df['DATE_DIFF'] <= days_after)]

    # Identify rows that match the specified treatment codes
    matches = df[index_code_ccam].isin(CCAM_codes) | df[index_code_atc].isin(ATC_codes) | df[index_code_icd].isin(ICD_Codes)
    
    # Filter the DataFrame to include only matching rows
    df_matches = df[matches]
    
    # Group by 'ID_PATIENT' and aggregate to find the minimum 'DATE' (i.e., the first treatment date) for each patient
    first_treatment_date = df_matches.groupby(index_id)[index_date].min().reset_index(name=column_name+' First_Treatment_Date')
    
    # Determine if each patient received any treatment by checking if they appear in the aggregated results
    result = df[index_date].drop_duplicates().reset_index(drop=True).to_frame()
    result = pd.merge(result, first_treatment_date, on=index_date, how='left')
    
    # Add a column indicating True if the patient received treatment (i.e., has a 'First_Treatment_Date') and False otherwise
    result[column_name] = result[column_name+' First_Treatment_Date'].notna()
    

    result = result[[index_date, column_name,column_name+ ' First_Treatment_Date']]
    
    # Fill NaN dates for patients without treatments
    result[column_name+' First_Treatment_Date'] = result[column_name+' First_Treatment_Date'].fillna('No Treatment')
        
    return result

def is_treated_by_it_with_qte(df, CCAM_codes, ATC_codes, ICD_Codes, column_name,  
                              index_code_ccam="CODE_CCAM", index_code_atc="CODE_ATC", 
                              index_code_icd="CODE_ICD10", index_id="ID_PATIENT", 
                              index_quantite="QUANTITE"):
    '''
    Determines if each patient in the DataFrame has received a treatment corresponding to any of the provided CCAM, ATC, or ICD codes and counts the number of relevant treatment sessions. Generates a summary DataFrame that includes each patient's ID and the number of treatment sessions.

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records. This DataFrame should include columns for patient ID (ID_PATIENT), treatment codes (CODE_CCAM, CODE_ATC, CODE_ICD10), and treatment dates (DATE). It also includes an alternate date column (DATE_ENTREE) for use when the DATE is missing.
    CCAM_codes : list
        A list of CCAM codes used to identify relevant treatments.
    ATC_codes : list
        A list of ATC codes used to identify relevant treatments.
    ICD_Codes : list
        A list of ICD codes used to identify relevant treatments.
    columnName : str
        A string specifying the name for the output column in the resulting DataFrame. This column will contain the number of treatment sessions for each patient.

    Returns
    -------
    DataFrame
        A DataFrame indicating the number of relevant treatment sessions for each patient.
    '''

    
    df[index_quantite] = df[index_quantite].fillna(1.0)
    df['SESSION'] = 1
    
    df['Is_Relevant'] = df[index_code_ccam].apply(starts_with_any, codes_list=CCAM_codes) | \
                    df[index_code_atc].apply(starts_with_any, codes_list=ATC_codes) | \
                    df[index_code_icd].apply(starts_with_any, codes_list=ICD_Codes)

    
    patient_classification = {}
    
    
    for patient_id in df[index_id].unique():
        # Filter the patient's relevant treatments
        patient_df = df[(df[index_id] == patient_id) & df['Is_Relevant']]

        # Skip patients with no relevant treatments
        if patient_df.empty:
            patient_classification[patient_id] = 0
            continue
        
        
        patient_classification[patient_id] = sum(patient_df['SESSION'])
            

    result = pd.DataFrame(list(patient_classification.items()), columns=[index_id, column_name])

    return result


def traitement_characterization(df, index_code_ccam="CODE_CCAM", 
                                index_code_atc="CODE_ATC", index_code_icd="CODE_ICD10", 
                                index_id="ID_PATIENT"):
    """
    Characterizes patient treatment data by calculating the percentage of patients treated with specific traitements.

    This function processes the treatment data from a global `data` dictionary and the input DataFrame `df` to determine
    the percentage of patients treated by various types of treatment and subcategories. It generates a DataFrame containing
    the treatment types, subcategories, and the corresponding treatment percentages.

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient records. It should include columns for patient IDs and medical codes.
    index_code_ccam : str, optional
        The name of the column in df that contains CCAM codes (default is "CODE_CCAM").
    index_code_atc : str, optional
        The name of the column in df that contains ATC codes (default is "CODE_ATC").
    index_code_icd : str, optional
        The name of the column in df that contains ICD10 codes (default is "CODE_ICD10").
    index_id : str, optional
        The name of the column in df that contains patient IDs (default is "ID_PATIENT").

    Returns
    -------
    DataFrame
        A DataFrame with columns "Treatment Type", "Subcategory", and "Percentage Treated". Each row represents a treatment
        type or subcategory and its associated percentage of patients treated.

    Raises
    ------
    ValueError
        If the global `data` dictionary does not contain the "Treatment" key or if "Treatment" is not a dictionary.
    """

    results = []


    if "Treatment" in data and isinstance(data["Treatment"], dict):

        for treatment_type, treatment_data in data['Treatment'].items():
            CODES_CCAM = data['Treatment'][treatment_type].get('CCAM', [])
            CODES_ATC = data['Treatment'][treatment_type].get('ATC', [])
            CODES_ICD10 = data['Treatment'][treatment_type].get('ICD10', [])

            # Store the "YES NO" percentage for the main treatment type
            main_result = is_treated_by_it_percentage(df, CODES_CCAM, CODES_ATC, CODES_ICD10,
                                                 index_code_ccam,index_code_atc,index_code_icd,index_id)


            results.append({
                "Treatment Type": treatment_type,
                "Subcategory": None,
                "Percentage Treated": main_result
            })

            if isinstance(treatment_data, dict):
                for category, codes in treatment_data.items():
                    if isinstance(codes, dict):

                        for sub_category, sub_codes in codes.items():
                            sub_CCM_codes = sub_codes.get('CCAM', [])
                            sub_ATC_codes = sub_codes.get('ATC', [])
                            sub_ICD_codes = sub_codes.get('ICD10', [])

                            sub_result = is_treated_by_it_percentage(df, sub_CCM_codes, sub_ATC_codes, sub_ICD_codes,
                                                                index_code_ccam,index_code_atc,index_code_icd,index_id)

                            results.append({
                                "Treatment Type": treatment_type,
                                "Subcategory": sub_category,
                                "Percentage Treated": sub_result
                            })

        df_results = pd.DataFrame(results)

        return df_results
    else:
        raise ValueError("The 'Treatment' section does not exist or is not a dictionary.")




def generate_patient_treatment_summary(df, listColumns,dateStart=None,dateEnd=None):
    '''
    Generates a merged DataFrame of patient treatments based on specified columns.

    The function checks the presence of specified columns in the DataFrame,
    counts the occurrences of unique values in each column.

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    listColumns : list of str
        A list of column names to process and merge based on their unique values.

    Returns
    -------
    DataFrame
        A merged DataFrame containing patient IDs and treatment information
        based on the specified columns.

    Raises
    ------
    ValueError
        If listColumns is empty or if any specified column is missing in the DataFrame.
    '''

        
    # Check if listColumns is empty
    if not listColumns:
        raise ValueError("listColumns cannot be empty.")
    
    # Check if all strings in listColumns are in df.columns
    missing_columns = [col for col in listColumns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"The following columns are missing in the DataFrame: {missing_columns}")
    
    if(dateStart!= None):
        base_date = pd.Timestamp(date(1960, 1, 1))
        dateStart = (pd.to_datetime(dateStart) - base_date)
        dateStart = dateStart.days
    
    if(dateEnd!= None):
        base_date = pd.Timestamp(date(1960, 1, 1))
        dateEnd = (pd.to_datetime(dateEnd) - base_date)
        dateEnd = dateEnd.days
    
    results = None
    
    for coln in listColumns:
        count = 0
        for i in df[coln].value_counts().index.tolist():
            if count == 0:
                results = is_treated_by_it_with_qte(df, i, i, i, i)
            else:
                r = is_treated_by_it_with_qte(df, i, i, i, i)
                results = pd.merge(results, r, on='ID_PATIENT')
            count += 1

    return results



def generate_act_sequences(df, list_columns,index_id="ID_PATIENT", index_date="DATE"):
    '''
    Generates a DataFrame with sequences of acts and dates for each patient based on specified columns.

    The function checks the presence of specified columns in the DataFrame,
    combines the codes from these columns into a single column, groups by patient ID,
    and sorts the acts by date.

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    listColumns : list of str
        A list of column names to process and combine into a sequence of acts.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and sequences of acts and dates.

    Raises
    ------
    ValueError
        If listColumns is empty or if any specified column is missing in the DataFrame.
    '''

        
    # Check if listColumns is empty
    if not list_columns:
        raise ValueError("listColumns cannot be empty.")
    
    # Check if all strings in listColumns are in df.columns
    missing_columns = [col for col in list_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"The following columns are missing in the DataFrame: {missing_columns}")
        
        
    def combine_codes(row):
        codes = ""
        for col in list_columns:
            if pd.notnull(row[col]):
                    codes = row[col]
        return codes

    # Apply the function to create CODE_ACTS
    df['CODE_ACTS'] = df.apply(combine_codes, axis=1)
    df = df[df['CODE_ACTS']!=""]
    df = df[[index_id, index_date, 'CODE_ACTS']]

    df = df.sort_values(by=[index_id, index_date])

    
    grouped = df.groupby(index_id).agg({index_date: list, 'CODE_ACTS': list}).reset_index()

    # Sort acts by date within each group
    grouped['ACTES'] = grouped.apply(lambda row: [act for _, act in sorted(zip(row[index_date], row['CODE_ACTS']))], axis=1)

    # Create the final DataFrame with ID_PATIENT, DATES, and ACTES columns
    final_df = grouped[[index_id, index_date, 'ACTES']]
    final_df.columns = [index_id, 'DATES', 'ACTES']
    
    return final_df


def generate_act_sequences_with_intervals(df, list_columns, index_id="ID_PATIENT", index_date="DATE"):
    '''
    Generates a DataFrame with sequences of acts and dates for each patient based on specified columns.

    The function checks the presence of specified columns in the DataFrame, combines the codes from these columns
    into a single column, groups by patient ID, sorts the acts by date, and creates sequences of [interval, CODE_ACTS].

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    listColumns : list of str
        A list of column names to process and combine into a sequence of acts.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and sequences of acts and dates.

    Raises
    ------
    ValueError
        If listColumns is empty or if any specified column is missing in the DataFrame.
    '''    
    # Check if listColumns is empty
    if not list_columns:
        raise ValueError("listColumns cannot be empty.")
    
    # Check if all strings in listColumns are in df.columns
    missing_columns = [col for col in list_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"The following columns are missing in the DataFrame: {missing_columns}")
        
        
    def combine_codes(row):
        codes = ""
        for col in list_columns:
            if pd.notnull(row[col]):
                    codes = row[col]
        return codes

    # Apply the function to create CODE_ACTS
    df['CODE_ACTS'] = df.apply(combine_codes, axis=1)
    df = df[df['CODE_ACTS']!=""]
    df = df[[index_id, index_date, 'CODE_ACTS']]
    
    # Sort the DataFrame by ID_PATIENT and DATE
    df = df.sort_values(by=[index_id, index_date])

    # Function to create the sequence for each patient
    def create_sequence(group):
        sequence = []
        prev_date = None
        for index, row in group.iterrows():
            if prev_date is None:
                prev_date = row[index_date]
                sequence.append(f"[0,{row['CODE_ACTS']}]")
            else:
                interval = row[index_date] - prev_date
                sequence.append(f"[{interval},{row['CODE_ACTS']}]")
                prev_date = row[index_date]
        return sequence

    # Group by ID_PATIENT and apply the function
    result = df.groupby(index_id).apply(create_sequence).reset_index()

    result.columns = [index_id, 'Sequence']
    
    return result


def neoadjuvant_or_adjuvant_or_both(df, CCAM_codes, ATC_codes, ICD_Codes, column_name, 
                                    days_before, days_after, index_date="DATE", 
                                    index_code_ccam="CODE_CCAM", index_code_atc="CODE_ATC", 
                                    index_code_icd="CODE_ICD10", index_id="ID_PATIENT", 
                                    bc_index_surgery="BC_index_surgery"):
    '''
    Evaluates patient treatment records to classify each patient's treatment as neoadjuvant, adjuvant, both, or not applicable.
    This classification is determined based on whether the treatments, identified by specific CCAM, ATC, or ICD codes,
    occurred within specified days before or after breast cancer surgery.

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records, including columns for patient ID (ID_PATIENT), treatment codes 
        (CODE_CCAM, CODE_ATC, CODE_ICD10), treatment dates (DATE), and an alternate date column (DATE_ENTREE) for use when the primary date is missing.
    CCAM_codes : list
        A list of CCAM codes identifying relevant treatments.
    ATC_codes : list
        A list of ATC codes identifying relevant treatments.
    ICD_Codes : list
        A list of ICD codes identifying relevant treatments.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating the classification of each patient's treatment relative to their surgery date.
    daysBefore : int
        The number of days before surgery within which treatments are considered neoadjuvant.
    daysAfter : int
        The number of days after surgery within which treatments are considered adjuvant.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and their treatment classification ('Neoadjuvant', 'Adjuvant', 'Both', or 'False').
    '''
    
    df['DATE_DIFF'] = df[index_date] - df[bc_index_surgery]
    
    df = df[(df['DATE_DIFF'] >= -days_before) & (df['DATE_DIFF'] <= days_after)]

    df['Is_Relevant'] = df[index_code_ccam].isin(CCAM_codes) | df[index_code_atc].isin(ATC_codes) | df[index_code_icd].isin(ICD_Codes)
    
    patient_classification = {}
    
    for patient_id in df[index_id].unique():
        # Filter the patient's relevant treatments
        patient_df = df[(df[index_id] == patient_id) & df['Is_Relevant']]

        # Skip patients with no relevant treatments
        if patient_df.empty:
            patient_classification[patient_id] = 'False'
            continue

        # Count positive and negative DATE_DIFF values
        positive_count = sum(patient_df['DATE_DIFF'] > 0)
        negative_count = sum(patient_df['DATE_DIFF'] < 0)
        
        # Classify based on the counts
        if positive_count > 0 and negative_count > 0:
            patient_classification[patient_id] = 'Both'
        elif positive_count > 0:
            patient_classification[patient_id] = 'Adjuvant'
        elif negative_count > 0:
            patient_classification[patient_id] = 'Neoadjuvant'
        else:
            patient_classification[patient_id] = 'False'
            

    result = pd.DataFrame(list(patient_classification.items()), columns=[index_id, column_name])

    return result

def chemotherapy_intervals(df, CCAM_codes, ATC_codes, ICD_Codes, column_name, days_before, days_after,
                           index_date="DATE", index_code_ccam="CODE_CCAM", index_code_atc="CODE_ATC", 
                           index_code_icd="CODE_ICD10", index_id="ID_PATIENT", bc_index_surgery="BC_index_surgery"):
    """
    Calculates the time intervals between chemotherapy treatments for each patient based on the specified codes 
    and within a given time window relative to a reference date.

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    ccam_codes : list
        A list of CCAM codes used to identify relevant chemotherapy treatments.
    atc_codes : list
        A list of ATC codes used to identify relevant chemotherapy treatments.
    icd_codes : list
        A list of ICD codes used to identify relevant chemotherapy treatments.
    column_name : str
        The name of the output column that will contain the time intervals between treatments.
    days_before : int
        The number of days before the index date to include in the time window.
    days_after : int
        The number of days after the index date to include in the time window.
    index_date : str, optional
        The column name representing the date of treatment (default is "DATE").
    index_code_ccam : str, optional
        The column name for CCAM codes in the DataFrame (default is "CODE_CCAM").
    index_code_atc : str, optional
        The column name for ATC codes in the DataFrame (default is "CODE_ATC").
    index_code_icd : str, optional
        The column name for ICD codes in the DataFrame (default is "CODE_ICD10").
    index_id : str, optional
        The column name for patient ID in the DataFrame (default is "ID_PATIENT").
    bc_index_surgery : str, optional
        The column name for the reference date (e.g., surgery date or another event) (default is "BC_index_surgery").

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a column containing the time intervals between chemotherapy treatments 
        as a string formatted with arrows indicating the time differences.
    
    Raises
    ------
    ValueError
        If any specified column is missing in the DataFrame.
    """

    
    df['DATE_DIFF'] = df[index_date] - df[bc_index_surgery]
    
    df = df[(df['DATE_DIFF'] >= -days_before) & (df['DATE_DIFF'] <= days_after)]
    
    df.sort_values(by=[index_id, index_date], inplace=True)
    
    df['Is_Relevant'] = df[index_code_ccam].isin(CCAM_codes) | df[index_code_atc].isin(ATC_codes) | df[index_code_icd].isin(ICD_Codes)
    
    patient_classification = {}
    
    
    for patient_id in df[index_id].unique():

        patient_df = df[(df[index_id] == patient_id) & df['Is_Relevant']]
        
        if patient_df.empty:
            patient_classification[patient_id] = 'False'
            continue
        
        Text = ""
        temp = 0
        c = 0
        for i ,data in patient_df.iterrows():
            if(c==0):
                Text = "0"
                temp = data[index_date]
            else:
                Text += " -> " + str(data[index_date]-temp)
                temp = data[index_date]
                
            c+=1
            
        patient_classification[patient_id] = Text
        
        
    result = pd.DataFrame(list(patient_classification.items()), columns=[index_id, column_name])


    return result

def classify_regimen_chemo(text):
    """
    Classifies chemotherapy regimens based on the intervals between treatment sessions provided in a text.

    The function analyzes a string representing the intervals between chemotherapy sessions. It converts these intervals into standardized values and then classifies the regimen into one of several categories based on the pattern of intervals.

    Parameters
    ----------
    text : str
        A string representing the intervals between chemotherapy sessions in days, separated by arrows (e.g., "0 -> 21 -> 7 -> 21").

    Returns
    -------
    str
        The classification of the chemotherapy regimen. Possible values are:
        - "False": No chemotherapy was done.
        - "ONE TREATMENT": Only one session of chemotherapy was recorded.
        - "Paclitaxel": Regimen consists entirely of 7-day intervals.
        - "Anthracyclines/docetaxel": Regimen has a pattern of 14-day intervals followed by 21-day intervals.
        - "Anthracyclines/paclitaxel": Regimen has a pattern of 14-day intervals followed by 7-day intervals.
        - "Anthracyclines/paclitaxel": Regimen has a pattern of 21-day intervals followed by 7-day intervals (in the case of transition).
        - "Anthracyclines": Regimen consists entirely of 21-day intervals.
        - "Other": Any regimen that does not fit the above categories.

    Notes
    -----
    - Intervals are normalized to specific values: 20 and 22 are treated as 21, 6 and 8 as 7, and 13 and 15 as 14.
    - The function uses regular expressions to extract numerical values from the input text.
    - The classification is based on specific patterns of treatment intervals that are typical of certain chemotherapy regimens.
    """

    #Never done a chemotherapy
    if(text=="False"):
        return text
    
    numbers = [float(num) for num in re.findall(r'\b\d+\.?\d*\b', text) if float(num) != 0]
    
    #They done only one chemotherapy session
    if(len(numbers)==0):
        return "ONE TREATMENT"
    
    numbers = [21 if num in [20, 22] else num for num in numbers] 
    numbers = [7 if num in [6, 8] else num for num in numbers] 
    numbers = [14 if num in [13, 15] else num for num in numbers] 

    
    def is_paclitaxel(seq): return all(num == 7 for num in seq)
    
    def is_anthracyclines_docetaxel(seq):
        return len(seq) >= 4 and all(num == 14 for num in seq[:3]) and all(num == 21 for num in seq[3:])
    
    def is_anthracyclines_paclitaxel(seq):
        return len(seq) >= 4 and all(num == 14 for num in seq[:3]) and all(num == 7 for num in seq[3:])
    
    def is_anthracyclines_paclitaxel2(seq):

        try:
            transition_index = next(i for i, num in enumerate(seq) if num == 7)
        except StopIteration:
            return False  # No 7-day interval found

        # Check if all intervals before transition are 21-day and after are 7-day
        before_transition = all(num == 21 for num in seq[:transition_index])
        after_transition = all(num == 7 for num in seq[transition_index:])

        return before_transition and after_transition

    def is_anthracyclines(seq): return all(num == 21 for num in seq) #Unknown after March 2012
    
    
    if is_paclitaxel(numbers): return 'Paclitaxel'
    if is_anthracyclines_docetaxel(numbers): return 'Anthracyclines/docetaxel'
    if is_anthracyclines_paclitaxel(numbers): return 'Anthracyclines/paclitaxel'
    if is_anthracyclines_paclitaxel2(numbers): return 'Anthracyclines/paclitaxel'
    if is_anthracyclines(numbers): return 'Anthracyclines'
    return 'Other'

