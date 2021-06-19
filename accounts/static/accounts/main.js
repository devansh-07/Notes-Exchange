function CastVoteUtil(flag, val, id) {
    var data = new FormData();

    data.append('flag', flag);
    data.append('vote', val);
    data.append('object_id', id);

	var xhr = new XMLHttpRequest();
    xhr.open('POST', '/cast-vote/', true);

	xhr.onload = function(){
		if (this.status == 201) {
            if (flag == '0') {
                var el = document.querySelector("#req-" + id);
                if (val == '1') {
                    // console.log();
                    console.log("Upvote for", "#req-" + id);
                } else {
                    console.log("Downvote for", "#req-" + id);
                }
            } else {
                var el = document.querySelector("#upload-" + id);
                if (val == '1') {
                    console.log("Upvote for", "#upload-" + id);
                } else {
                    console.log("Downvote for", "#upload-" + id);
                }
            }
		}
	}

	xhr.send(data);
}
