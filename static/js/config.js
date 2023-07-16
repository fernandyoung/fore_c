const range = document.getElementById('range');
const c = document.getElementById('c');
const e = document.getElementById('epsilon');

range.addEventListener('change', updateSelectedValues);
c.addEventListener('change', updateSelectedValues);
e.addEventListener('change', updateSelectedValues);

function updateSelectedValues(){
	const sRange = range.value;
	const sC = c.value;
	const sE = e.value;

	const xhr = new XMLHttpRequest();
	xhr.open('POST', '/');
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.send(JSON, stringfy({
		'range': sRange,
		'c' : sC,
		'e' : sE
	}))
}