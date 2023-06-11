
    document.title = "procject-3 Percent of adults aged 18 years and older who have obesity";
    var cPrev = -1;
    window.onload =  getDataFromPython;
    var states = [
            'Alaska',	
            'Arizona',	
            'Arkansas',	
            'California',	
            'Colorado',	
            'Connecticut',	
            'Delaware',	
            'Florida',	
            'Georgia',	
            'Hawaii',	
            'Idaho',	
            'Illinois',	
            'Indiana',	
            'Iowa',	
            'Kansas',	
            'Kentucky',	
            'Louisiana',	
            'Maine',	
            'Maryland',	
            'Massachusetts',	
            'Michigan',	
            'Minnesota',	
            'Mississippi',	
            'Missouri',	
            'Montana',	
            'Nebraska',	
            'Nevada',	
            'New Hampshire',	
            'New Jersey',	
            'New Mexico',	
            'New York',	
            'North Carolina',
            'North Dakota','Ohio',	
            'Oklahoma',	
            'Oregon',
            'Pennsylvania',	
            'Rhode Island',
            'South Carolina',
            'South Dakota',
            'Tennessee',
            'Texas',
            'Utah',
            'Vermont',
            'Virginia',
            'Washington',
            'West Virginia',
            'Wisconsin',
            'Wyoming',
            'American Samoa',
            'District of Columbia',
            'Federated States of Micronesia',
            'Guam',
            'Marshall Islands',
            'Northern Mariana Islands',
            'Palau',
            'Puerto Rico',
            'Virgin Islands'
        ]

    eel.expose(getDataFromPython);
    async function getDataFromPython() {
        globalThis.data = await eel.collectData()(); //needs to be a global var so we can access it from any function. 
        iterateDict();
        populateYear();
    };

    eel.expose(updateMessage);
    function updateMessage(message) {
        document.getElementById("onPageMessage").innerHTML = message;
    };
    async function getLocalPath() {
        path = await eel.getLocalPath()(); 
        return(path);
    };

    async function preDeleteDatabaseHTML() {
        loc = await eel.getLocalPath()();
        deleteDatabaseHTML(loc);
    }

    function clearAllDivs() {
        document.getElementById("mapDiv").innerHTML ="";
        document.getElementById("plot").innerHTML ="";
        document.getElementById("plot2").innerHTML ="";
        document.getElementById("plot3").innerHTML ="";
        document.getElementById("onPageMessage").innerHTML ="";
        document.getElementById("table").innerHTML ="";
    }

    function deleteDatabaseHTML(loc) {
        mes = "Delete " + loc + "?";
        if (confirm(mes)) {
            clearAllDivs();
            eel.deleteDatabase();
        } else {
            document.getElementById("onPageMessage").innerHTML = "SELECT YEAR OR STATE BELOW";
        }
    };

    function iterateDict(){
        var options = ['','2011', '2012','2013','2014','2015','2016','2017','2018','2019','2020', '2021'];
        var select = document.getElementById("selYear");
        for(var i = 0; i < options.length; i++) {
            var opt = options[i];
            var el = document.createElement("option");
            el.textContent = opt;
            el.value = opt;
            select.appendChild(el);
        }
    };

    function populateYear(){
        var listOfActualStates = [];
        data.forEach((element) => {
            listOfActualStates.push(element.LocationDesc);
        });
        const uniqueActualStates = listOfActualStates.filter((value, index) => listOfActualStates.indexOf(value) === index);
        uniqueActualStates.unshift("");
        stateSelected = document.getElementById("selState");
        for(var i = 0; i < uniqueActualStates.length; i++) {
            var opt = uniqueActualStates[i];
            var el = document.createElement("option");
            el.textContent = opt;
            el.value = opt;
            stateSelected.appendChild(el);
        }
    };

    function stOptionChanged(stateSelected){
        document.getElementById("onPageMessage").innerText = "";
        if (stateSelected == ""){
            document.getElementById("mapDiv").innerText = "";
            return
        }
        var wholeThingList = [];
        data.forEach((element) => {
            tempList = [];
            if (element.LocationDesc == stateSelected){
                for (const [key, value] of Object.entries(element)) {
                    // console.log(`${key}: ${value}`);
                    tempList.push(value);
                };
                wholeThingList.push(tempList);
            }
        
        });

        question = [];
        wholeThingList.forEach((el) => {
            q = el[2];
            tempList = [];
            if (q.includes("Percent of adults aged 18 years and older who have obesity")){
                year = el[0];
                state = el[1];
                percentage = el[3];
                ageRange = el[4];
                coordinates = el[5];
                tempList.push([q,year,state,percentage,ageRange,coordinates]);
            }   
            question.push(tempList);
        });

        var result = "<table id='sortable' border=1> <thead> <tr><th onclick='sortBy(0)'>YEAR</th><th onclick='sortBy(1)'>State</th><th onclick='sortBy(2)'>Question</th><th onclick='sortBy(3)'>Percentage</th><th onclick='sortBy(4)'>Age Range</th><th onclick='sortBy(5)'>Coordinates</th></tr></thead>";
            for(var i=0; i<wholeThingList.length; i++) {
                result += "<tr>";
                for(var j=0; j<wholeThingList[i].length; j++){
                    result += "<td>"+wholeThingList[i][j]+"</td>";
                }
                result += "</tr>";
            }
            result += "</table>";
        document.getElementById("table").innerHTML = result;

        addMap(coordinates);
        createPieChartForState(stateSelected);
    };

    function addMap(coordinates) {
        var cordinates = coordinates.split(",");
        var lat = coordinates.split("(");
        lat = cordinates[0].replace("(", "");
        lon = cordinates[1].replace(")", "");
        lat1 = parseFloat(lat);
        lon1 = parseFloat(lon);
        var container = L.DomUtil.get('mapDiv');
        if(container != null){
        container._leaflet_id = null;
        }
        var map = L.map('mapDiv').setView([lat1, lon1], 13);
        map.setZoom(7);
        L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {
            maxZoom: 7,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &amp; USGS',

        }).addTo(map);
    };

    function optionChanged(yearSelected) {
        document.getElementById("onPageMessage").innerText = "";
        if (yearSelected == ""){
            document.getElementById("plot").innerText = "";
            document.getElementById("plot2").innerText = "";
            document.getElementById("plot3").innerText = "";
            return
        }
        addPlot(yearSelected);
        createPieChart(yearSelected);
    };

    function addPlot(yearSelected) {
        ySelectedArray = [];
        yearAgeRange = [];
        data.forEach((element) => {
            if (element.YearEnd == yearSelected){
                ySelectedArray.push(element);
                yearAgeRange.push(element.Age_year)
            }
        });
        var dictOfStates = {};
        var dictofRanges = {};

        states.forEach((st) => {
            dataValue = 0
                count = 0
            ySelectedArray.forEach((element) => {  
                if (element.LocationDesc == st ){
                    count = count + 1
                    dataValue = Number(dataValue) + Number(element.Data_Value)
                }
                dVal = (Number(dataValue) / Number(count));
                if (dVal == "NaN"){
                    dVal = "0";
                }   
                dictOfStates[st] = dVal .toFixed(2);
            });
        });
        const sortedByVal = Object.fromEntries(
            Object.entries(dictOfStates).sort(([,a],[,b]) => a-b)
        );

        xval = [];
        yval = []
        for (const [key, value] of Object.entries(sortedByVal)) {
            // console.log(`${key}: ${value}`);
            if (isNaN(value)){
                continue;
            }
            xval.push(value);
            yval.push(key);
        };

        let trace = {
            y: xval,
            x: yval,
            lable: yearSelected,
            
            type: 'bar',
            // orientation:"h",
            mode: 'lines+markers',
            marker: { color: "cyan-blue" },
        };

        let layout = {
            margin: { 
                t:25, 
                b:150,
                l: 25,
                r: 50,
            },
            width: 1255,
            height: 500,
            title: "COMBINED PERCENTAGE (AVE) PER STATE FOR THE YEAR " + yearSelected 
        };
        Plotly.newPlot("plot", [ trace ], layout);
    };

    function sortBy(c) {
    rows = document.getElementById("sortable").rows.length; // num of rows
    columns = document.getElementById("sortable").rows[0].cells.length; // num of columns
    arrTable = [...Array(rows)].map(e => Array(columns)); // create an empty 2d array

    for (ro=0; ro<rows; ro++) { // cycle through rows
        for (co=0; co<columns; co++) { // cycle through columns
            // assign the value in each row-column to a 2d array by row-column
            arrTable[ro][co] = document.getElementById("sortable").rows[ro].cells[co].innerHTML;
        }
    }

    th = arrTable.shift(); // remove the header row from the array, and save it
    if (c !== cPrev) { // different column is clicked, so sort by the new column
        arrTable.sort(
            function (a, b) {
                if (a[c] === b[c]) {
                    return 0;
                } else {
                    return (a[c] < b[c]) ? -1 : 1;
                }
            }
        );
    } else { // if the same column is clicked then reverse the array
        arrTable.reverse();
    }
    
    cPrev = c; // save in previous c
    arrTable.unshift(th); // put the header back in to the array
    // cycle through rows-columns placing values from the array back into the html table
    for (ro=0; ro<rows; ro++) {
        for (co=0; co<columns; co++) {
            document.getElementById("sortable").rows[ro].cells[co].innerHTML = arrTable[ro][co];
        }
    }
};

function createPieChart(yearSelected) {
    xValues = []; 
    yValues = [];

    data.forEach((row) => {
        if (row.YearEnd == yearSelected){
            xValues.push(row.Data_Value);
            yValues.push(row.Age_years);
        }
    });

    var data1 = [{
        values: xValues,
        labels: yValues,
        type: 'pie',
        title: yearSelected +' - Per Age'
    }];

    var layout = {
        height: 400,
        width: 400
    };
    Plotly.newPlot('plot2', data1, layout);
};

function createPieChartForState(stateSelected) {
    xValues = []; 
    yValues = [];
    data.forEach((row) => {
        if (row.LocationDesc == stateSelected){
            xValues.push(row.Data_Value);
            yValues.push(row.Age_years);
        }
    });
    var dat = [{
        values: xValues,
        labels: yValues,
        type: 'pie',
        title: stateSelected +' - Per Age'
    }];

    var layout = {
        height: 400,
        width: 400
    };
    Plotly.newPlot('plot3', dat, layout);
};