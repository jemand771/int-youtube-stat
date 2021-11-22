    function deleteAllElements() {
        let parent = document.getElementsByClassName("scroll-box")[0];
        while (parent.firstChild) parent.removeChild(parent.firstChild);
    }
