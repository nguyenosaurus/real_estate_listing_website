// File javascript để lấy dữ liệu

var provinceUrl = "/province";
var districtUrl = "/district";
var wardUrl = "/ward";
$(document).ready(function () {
    // load province list
    _getProvince();

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
    $("#ddlWard").on('change', function () {
        var provinceText = $("#ddlProvince option:selected").text().toLowerCase().replace(/(huyện |thành phố |thị xã |quận |phường |thị trấn |xã |tỉnh )/,'');
        var districtText = $("#ddlDistrict option:selected").text().toLowerCase().replace(/(huyện |thành phố |thị xã |quận |phường |thị trấn |xã |tỉnh )/,'');
        var wardText = $("#ddlWard option:selected").text().toLowerCase().replace(/(huyện |thành phố |thị xã |quận |phường |thị trấn |xã |tỉnh )/,'');
        window.location.href = "/?province="+provinceText+"&district="+districtText+"&ward="+wardText;
    });
});

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