let botonEuskera = document.getElementById('btn-euskera');
let botonCastellano = document.getElementById('btn-castellano');

// Oculta las letras en las que no queda ningún término visible.
// claseOculta es la clase de los términos que no existen en ese idioma.
function ocultarLetrasVacias(claseOculta) {
    let grupos = document.querySelectorAll('.grupo-letra');

    for (let i = 0; i < grupos.length; i++) {
        let terminos = grupos[i].getElementsByTagName('li');
        let hayVisibles = false;

        for (let j = 0; j < terminos.length; j++) {
            if (!terminos[j].classList.contains(claseOculta)) {
                hayVisibles = true;
            }
        }

        if (hayVisibles) {
            grupos[i].style.display = '';
        } else {
            grupos[i].style.display = 'none';
        }
    }
}

let enDiccionario = document.getElementById('pagina-diccionario') !== null;
let enDetalle = document.getElementById('pagina-detalle') !== null;

// Solo en el diccionario y en la página de cada término se puede cambiar de idioma
if (!enDiccionario && !enDetalle) {
    botonEuskera.style.display = 'none';
} else {
    ocultarLetrasVacias('solo-eu');

    botonEuskera.addEventListener('click', function () {
        document.body.classList.add('euskera');
        botonEuskera.classList.add('activo');
        botonCastellano.classList.remove('activo');
        ocultarLetrasVacias('solo-es');
    });

    botonCastellano.addEventListener('click', function () {
        document.body.classList.remove('euskera');
        botonCastellano.classList.add('activo');
        botonEuskera.classList.remove('activo');
        ocultarLetrasVacias('solo-eu');
    });
}