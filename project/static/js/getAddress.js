// File javascript để lấy dữ liệu

var provinceUrl = "/province";
var districtUrl = "/district";
var wardUrl = "/ward";
var projectUrl = "/project";
var propertyUrl = "/property";
var transactionUrl = "/transaction"
$(document).ready(function () {
    // load province list
    _getProvince();
    _getProject();
    _getProperty();
    _getTransaction();

    $("#ddlProvince").on('change', function () {
        var id = $(this).val();
        if (id != undefined && id != '') {
            _getDistrict(id);
        }
    });
    $("#ddlDistrict").on('change', function () {
        var district_id = $(this).val();
        var city_id = $("#ddlProvince").val();
        if (district_id != undefined && district_id != '' && city_id != undefined && city_id != '') {
            _getWard(city_id, district_id);
        }
    });
    $("#search").on('click', function () {
        var provinceText = $("#ddlProvince option:selected").val().toLowerCase().replace(/(huyện |thành phố |thị xã |quận |phường |thị trấn |xã |tỉnh )/,'');
        var districtText = $("#ddlDistrict option:selected").val().toLowerCase().replace(/(huyện |thành phố |thị xã |quận |phường |thị trấn |xã |tỉnh )/,'');
        var wardText = $("#ddlWard option:selected").val().toLowerCase().replace(/(huyện |thành phố |thị xã |quận |phường |thị trấn |xã |tỉnh )/,'');
        var projectText = $("#project option:selected").val();
        var propertyText = $("#property_type option:selected").val();
        var transactionText = $("#transaction_type option:selected").val();
        window.location.href = "/?province="+provinceText+"&district="+districtText+"&ward="+wardText+"&project_id="+projectText+"&property_type_id="+propertyText+"&transaction_type_id="+transactionText;
    });
});

function _getProject() {
    $.get(projectUrl, function (data) {
        if (data != null && data != undefined) {
            var html = '';
            html += '<option value="">--Không chọn--</option>';
            $.each(data, function (key, item) {
                html += "<option value='" + key + "'>" + item + '</option>';
            });
            $("#project").html(html);
        }
    });
}

function _getProperty() {
    $.get(propertyUrl, function (data) {
        if (data != null && data != undefined) {
            var html = '';
            html += '<option value="">--Không chọn--</option>';
            $.each(data, function (key, item) {
                html += "<option value='" + key + "'>" + item + '</option>';
            });
            $("#property_type").html(html);
        }
    });
}

function _getTransaction() {
    $.get(transactionUrl, function (data) {
        if (data != null && data != undefined) {
            var html = '';
            html += '<option value="">--Không chọn--</option>';
            $.each(data, function (key, item) {
                html += "<option value='" + key + "'>" + item + '</option>';
            });
            $("#transaction_type").html(html);
        }
    });
}

function _getProvince() {
    $.get(provinceUrl, function (data) {
        if (data != null && data != undefined && data.length) {
            var html = '';
            html += '<option value="">--Không chọn--</option>';
            $.each(data, function (key, item) {
                html += "<option value='" + item + "'>" + item + '</option>';
            });
            $("#ddlProvince").html(html);
        }
    });
}
// pass province id
function _getDistrict(id) {
    $.get(districtUrl, {id: id}, function (data) {
        if (data != null && data != undefined && data.length) {
            var html = '';
            html += '<option value="">--Không chọn--</option>';
            $.each(data, function (key, item) {
                html += "<option value='" + item + "'>" + item + '</option>';
            });
            $("#ddlDistrict").html(html);
        }
    });
}
// pass city id and district id
function _getWard(city_id, district_id) {
    $.get(wardUrl, {district_id: district_id, city_id: city_id}, function (data) {
        if (data != null && data != undefined && data.length) {
            var html = '';
            html += '<option value="">--Không chọn--</option>';
            $.each(data, function (key, item) {
                html += "<option value='" + item + "'>" + item + '</option>';
            });
            $("#ddlWard").html(html);
        }
    });
}