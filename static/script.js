

var air_data = [[[[-1, -1, ''], [-1, -1, ''], [-1, -1, ''], [-1, -1, '']],
                 [[-1, -1, ''], [-1, -1, ''], [-1, -1, ''], [-1, -1, '']],
                 [[-1, -1, ''], [-1, -1, ''], [-1, -1, ''], [-1, -1, '']]],
                [[[-1, -1, ''], [-1, -1, ''], [-1, -1, ''], [-1, -1, '']],
                 [[-1, -1, ''], [-1, -1, ''], [-1, -1, ''], [-1, -1, '']],
                 [[-1, -1, ''], [-1, -1, ''], [-1, -1, ''], [-1, -1, '']]]];
var index = 0;
var floor = 2;

function update_table() {

    // wing A
    wing_a = document.getElementsByClassName("a");
    wing_a[0].innerHTML = air_data[index][floor][0][0]; // average
    wing_a[1].innerHTML = air_data[index][floor][0][1]; // maximum
    wing_a[2].innerHTML = air_data[index][floor][0][2]; // room name of the maximum

    // wing B
    wing_b = document.getElementsByClassName("b");
    wing_b[0].innerHTML = air_data[index][floor][1][0]; // average
    wing_b[1].innerHTML = air_data[index][floor][1][1]; // maximum
    wing_b[2].innerHTML = air_data[index][floor][1][2]; // room name of the maximum

    // wing C
    wing_c = document.getElementsByClassName("c");
    wing_c[0].innerHTML = air_data[index][floor][2][0]; // average
    wing_c[1].innerHTML = air_data[index][floor][2][1]; // maximum
    wing_c[2].innerHTML = air_data[index][floor][2][2]; // room name of the maximum

    // wing D
    wing_d = document.getElementsByClassName("d");
    wing_d[0].innerHTML = air_data[index][floor][3][0]; // average
    wing_d[1].innerHTML = air_data[index][floor][3][1]; // maximum
    wing_d[2].innerHTML = air_data[index][floor][3][2]; // room name of the maximum
}

function switch_data(button_id) {
    if(button_id == "co2"){
        document.getElementById("temp").checked = "";
        document.getElementById("co2").checked = "checked";
        index = 1; // switch to co2
    }
    else
    {
        document.getElementById("temp").checked = "checked";
        document.getElementById("co2").checked = "";
        index = 0; // switch to temp
    }

    update_table();
}

function switch_floor(floor_id) {
    floor_char = floor_id[floor_id.length - 1];
    floor = parseInt(floor_char);

    document.getElementById("floor0").checked = "";
    document.getElementById("floor1").checked = "";
    document.getElementById("floor2").checked = "";

    document.getElementById(floor_id).checked = "checked";
    update_table();

    update_floor(floor);
    update_table();
}

function update_all_data() {
    $.ajax({
      dataType: "json",
      url: "/update_all",
      data: {},
      async: true,
      success: function(data, textStatus, jqXHR) {
        console.log("all updated data recieved");
        air_data = data;
        document.getElementsByTagName("header").innerHTML = "";
        update_table();
        }
    });
}

function update_specific(selected_wing, selected_floor) {
    $.ajax({
      dataType: "json",
      url: "/update_area",
      data: {wing: selected_wing, floor: selected_floor},
      async: true,
      success: function(data, textStatus, jqXHR) {
        console.log("updated specific area data recieved");
        // update air_data with the new data
        air_data = data;
        document.getElementsByTagName("header").innerHTML = "";
        update_table();
        }
    });
}

function update_floor(selected_floor) {
    $.ajax({
      dataType: "json",
      url: "/update_floor",
      data: {floor: selected_floor},
      async: true,
      success: function(data, textStatus, jqXHR) {
        console.log("updated floor data recieved");
        // update air_data with the new data
        air_data = data;
        document.getElementsByTagName("header").innerHTML = "";
        update_table();
        }
    });
}

function load_data() {
//    air_data = JSON.parse(document.getElementById("data_transfer").innerHTML);
    $.ajax({
      dataType: "json",
      url: "/load_saved_data",
      data: {},
      async: false,
      success: function(data, textStatus, jqXHR) {
        console.log("saved data recieved");
        air_data = data;
        document.getElementsByTagName("header").innerHTML = "";
        update_table();
        }
    });
}

// The sleep function was copied from stackoverflow
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function background_update() {
    while(true) {
        await sleep(18000000);
        update_table();
        update_all_data();
    }
}

$(document).ready(function() {
    console.log("Document ready");
    load_data();
    update_table();

    switch_floor("floor2");

    background_update();
});

