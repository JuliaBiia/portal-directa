const getCookie = name => {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

const retornarValueCampoData = seletor => {
    let data = document.querySelector(`${seletor}`).value.split("/");
	data = `${data[2]}-${data[1]}-${data[0]}`;

    return data;
}