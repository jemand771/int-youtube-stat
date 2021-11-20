let inputForm = document.getElementsByTagName("form")[0];
inputForm.addEventListener('submit', (event) => {
    event.preventDefault();
    fetch("/video_data/"+document.getElementById("lk").value)
    .then(res => res.json())
    .then((out) => {
        console.log('Output: ', out);
        createVideoObjects(out);
    }).catch(err => console.error(err));
    });
