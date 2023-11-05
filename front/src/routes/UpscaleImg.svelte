<head>
    <script src="https://www.google.com/recaptcha/api.js"></script>
</head>
<script>
    import imageIcon from "../lib/image-file-svgrepo-com.svg";

    let file = ''
    let scale = ''
    let algorithm = ''
    let resultFilename=''
    let v = ''

    const check_recaptcha = () =>{
        v = grecaptcha.getResponse();
        if (v.length ==0) {
            alert ("'로봇이 아닙니다.'를 체크해주세요.");
            return false;
        } else {
            return true;
        }
    }

    const handleFileChange = async (e) => {
        if(check_recaptcha()){
            const imgFormData = new FormData();
            imgFormData.append("file",file);
            imgFormData.append("scale",scale)
            imgFormData.append("algorithm",algorithm)
            imgFormData.append("v", v)

            const response = await fetch("http://127.0.0.1:8000/upscale",{
                method: "POST",
                headers: {
                    enctype: 'multipart/form-data', // 파일 형식 확인
                },
                body:imgFormData
            });

            let data = await response.json()
            resultFilename = data['result']

            if (response.ok){
                let resultDiv = document.getElementById('result')
                resultDiv.removeAttribute('style')

                let btn = document.createElement('button')
                btn.setAttribute('type', 'button')
                btn.setAttribute('class', 'download')
                btn.setAttribute('style', 'font-size: 1.5rem; font-weight: bold;')
                btn.setAttribute('onclick','location.href="http://127.0.0.1:8000/images/'+resultFilename+'"')
                btn.textContent = '다운로드'

                resultDiv.appendChild(btn)
            }
        }
    }

	let fileinput, preview;

	const onFileSelected =(e)=>{
    let image = e.target.files[0];
    file = e.target.files[0]
    let reader = new FileReader();
    reader.readAsDataURL(image);
    reader.onload = e => {
       preview = e.target.result
    };
}

</script>
<div id="app">
	<h1>이미지 업스케일</h1>

        {#if preview}
        <img class="preview" src="{preview}" alt="d" />
        {:else}
        <img class="preview" src="{imageIcon}" alt="" />
        {/if}
        <br/>
        <button class="upload" on:click={()=>{fileinput.click();}}>업로드</button>
      <br/>
      <div style="display: flow">
          알고리즘
          <input type="radio" bind:group={algorithm} value="ESPCN" checked/> edsr
          <input type="radio" bind:group={algorithm} value="FSRCNN" > fsrcnn
          <br/>
          배율
      <input type="radio" bind:group={scale} value="2x" checked/> 2x <input type="radio" bind:group={scale} value="3x"/> 3x <input type="radio" bind:group={scale} value="4x"/> 4x
      </div>
    <br/>
    <div class="g-recaptcha" data-sitekey="6Ley0fcoAAAAAH1e7WLx-a9LETWELDCw7WxHjwA1"></div>
    <input style="display:none" type="file" accept=".jpg, .jpeg, .png" on:change={(e)=>onFileSelected(e)} bind:this={fileinput}>
    <br/>
    <button class="convertBtn" type="button" on:click={handleFileChange}>업스케일</button>
    <br/>
    <div id="result" style="display:none"></div>
</div>
<style>
	#app{
	    display:flex;
		align-items:center;
		justify-content:center;
		flex-flow:column;
    }

    .convertBtn {
        color: black;
        background-color: gold;
    }

	.upload {
        color: white;
        background-color: blue;
    }
	.preview{
		display:flex;
		height:200px;
		width:200px;
	}
</style>