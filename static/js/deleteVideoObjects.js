    function removeChildElement(childElement) {
        childElement.parentElement.remove();
        updateStatistics();
        if (document.getElementsByClassName("single-video-container").length == 0) {
            resetStatistics();
        }
    }

    function deleteAllElements() {
        let parent = document.getElementsByClassName("scroll-box")[0];
        while (parent.firstChild) parent.removeChild(parent.firstChild);
        resetStatistics();
    }
