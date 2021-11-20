let inputForm = document.getElementsByTagName("form")[0];
inputForm.addEventListener('submit', (event) => {
    event.preventDefault();
    let url = '/video_ids/path=';
    url += document.getElementById("lk").value;
    var oReq = new XMLHttpRequest();
    oReq.open("GET", url);
    // retrieve data unprocessed as a binary string
    oReq.overrideMimeType("text/plain; charset=x-user-defined");
    oReq.send();
  });
