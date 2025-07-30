
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

###########   histogram  ###############

def histogram(df,            # whole dataframe
              column,        # which column to plot
              bins,          # boundaries, including the left-m0st and right-most
              title = None,  # title of the whole plot
              wantPercentage = False,
              wantAverage = False):    
    if title == None: title = column
    
    fig, ax = plt.subplots(1,1)  # add a new figure to the plot
    plt.tight_layout()           # Fill the whole figure

    # The meat -- calculate the histogram        
    (values,                                   # value for each bin
     bins,                                     # returns the bins
     patches) = ax.hist(                       # patches are graphic objects representing the bars 
         df[column], bins = bins,
         rwidth           = 0.8,               # width of the bars
         color            = 'cyan',            # fill color of the bars
         edgecolor        = 'red',             # edge color of the bars
         alpha            = 0.9)               # transparency of the bars

    
    plt.xticks(bins, rotation=0, ha='center')  # label x-axis with the boundaries of the bins
    plt.grid(axis='x', alpha=0)                # no vertical grid lines
    plt.grid(axis='y', alpha=0.2)              # faint horizontal grid lines
    


    total = sum(values)
    
    # Add the frequency count on top of each bar
    # and percentage at the bottom
    for i, patch in enumerate(patches):
        x_val = patch.get_x() + patch.get_width() / 2  # Center of the bar
        y_val = patch.get_height()                     # Top of the bar
        
        val = values[i]
        plt.text(x_val, y_val, int(val),  ha='center', va='bottom', fontsize=9, color='black')
        if wantPercentage and y_val > 2:  # do it only if the bar is high enough
            percent = "%3.1f%%" % (100*val/total)
            plt.text(x_val, 0, percent, ha='center', va='bottom', fontsize=9, color='black')
            
       
    # Add labeling
    plt.title("HISTOGRAM OF " + title.upper())
    plt.xlabel(title.capitalize())
    plt.ylabel("Number of students")

    if wantAverage:
        average = df[column].mean()   # determines x-coordinate of the symbol
        plt.text(average, 0, 'Δ', ha='center', va='top', fontsize=28, color='black') #non-ascii
        
        median  = df[column].median()
        plt.text(median,  -10, 'I', ha='center', va='bottom', fontsize=28, color='black')         

###########   pie chart  ###############

def pie(df,            # whole dataframe
        column,        # which column to plot
        labels,        # names of the categories
        bins = None,          # boundaries, including the left-most and right-most
        title = None): # title of the whole plot
    if title == None: title = column


    if bins == None:
        binned_data = df[column]
    else:
        # Rearange the data according how they belong to the bins
        binned_data = pd.cut(df[column], bins=bins, right=False)  # `right=False` means [left, right)

    # For each bin, count inside the bin
    # sort_index() ensures that the values are in order of the bins, not sorted by size
    frequencies = binned_data.value_counts().sort_index()

    fig, ax = plt.subplots(1,1)   # add a new figure to the plot
    
    plt.pie(frequencies.values, labels=labels, autopct='%1.1f%%')  # plot the pie chart
    plt.title("PIE CHART OF " + title.upper())
    
    


###########   pie chart  ###############

def pieC(df,            # whole dataframe
        column,        # which column to plot
         labels,
         title = None): # title of the whole plot
    if title == None: title = column

    # For each bin, count inside the bin
    # sort_index() ensures that the values are in order of the bins, not sorted by size
    frequencies = df[column].value_counts()

    fig, ax = plt.subplots(1,1)   # add a new figure to the plot
    
    plt.pie(frequencies.values, labels=labels, autopct='%1.1f%%')  # plot the pie chart
    plt.title("PIE CHART OF " + title.upper())
    
    


###########   main  ###############


np.random.seed(2)

nF                = 900  # number of females
nM                = 500  # number of males

heightMeanMale   = 5.7
heightMeanFemale = 5.3
heightStd        = 0.15
heightBins       = [4.8, 4.9, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6, 6.1, 6.2]

weightMeanMale   = 160
weightMeanFemale = 140
weightStd        = 10
weightBins       = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190]
weightBinsFine   = [100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190]
weightBinsFinest = [i for i in range(105, 190)]

BMIbins          = [15, 18.5, 25, 30, 40]
gradeBins        = [50,  60,  73,  90, 100]
gradeLabels      = ["D", "C", "B", "A"]
genderLabels     = ["Female", "Male"]
# Create DataFrame
df = pd.DataFrame({
    'Gender'    : ['F' for i in range(nF)] + ['M' for i in range(nM)],
    'Height'    : np.concatenate([np.random.normal(heightMeanFemale, heightStd, nF),
                                  np.random.normal(heightMeanMale,   heightStd, nM)]),
    'Weight'    : np.concatenate([np.random.normal(weightMeanFemale, weightStd, nF),
                                  np.random.normal(weightMeanMale,   weightStd, nM)]),
    
    'Year'      : [np.random.randint( 9,  13) for i in range(nF+nM)],
    'Math'      : [np.random.randint(50, 100) for i in range(nF+nM)],
    'English'   : [np.random.randint(50, 100) for i in range(nF+nM)],
    'Soc.Study' : [np.random.randint(50, 100) for i in range(nF+nM)],
    'Phys.Ed'   : [np.random.randint(50, 100) for i in range(nF+nM)]
})

# Print the data frame with rounded height nd weight

dfRounded = df.round({'Height': 1})                    # Height 5.3
dfRounded['Weight'] = dfRounded['Weight'].astype(int)  # Weight is integer number of lb
pd.set_option('display.max_rows', None)                # print all rows
#print(dfRounded)


# Add BMI column
kgPerLb = 0.45359237
mPerFoot = 0.3048
df['BMI'] = df['Weight']*kgPerLb / (df['Height']*mPerFoot)**2

dfM = df[df['Gender'] == 'M'] # subframe of males   only
dfF = df[df['Gender'] == 'F'] # subframe of females only
 
histogram(df,  'Height', heightBins,              title="Height",        wantPercentage=True, wantAverage=True)
#histogram(df,  'BMI',       BMIbins,              title="BMI",           wantPercentage=False, wantAverage=False)
#histogram(df,  'Math',    gradeBins,              title="Math grades",   wantPercentage=False, wantAverage=False)
#pie(      df,  'Math',   gradeLabels, bins = gradeBins, title="Math grades")
#pie(      df,  'Gender', genderLabels,                  title="Gender distribution")
histogram(df,  'Weight', weightBins,                                     wantPercentage=True, wantAverage=True)
#histogram(df,  'Weight', weightBinsFine,          title="finer weight",  wantPercentage=False, wantAverage=False)
#histogram(df,  'Weight', weightBinsFinest,        title="finest weight", wantPercentage=False, wantAverage=False)

#histogram(dfM, 'Height', heightBins,              title="male height",   wantPercentage=True, wantAverage=True)
#histogram(dfF, 'Height', heightBins,              title="female height", wantPercentage=True, wantAverage=True)
#histogram(dfM, 'Weight', weightBins,              title="male weight",   wantPercentage=False, wantAverage=False)
#histogram(dfF, 'Weight', weightBins,              title="female weight", wantPercentage=False, wantAverage=False)

plt.show()



