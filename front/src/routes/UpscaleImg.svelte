<script>
    import imageIcon from "../lib/image-file-svgrepo-com.svg";

    let file = ''
    let scale = ''
    let algorithm = ''

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
          <input type="radio" bind:group={algorithm} value="edsr" checked/> edsr
          <input type="radio" bind:group={algorithm} value="fsrcnn" > fsrcnn
          <br/>
          배율
      <input type="radio" bind:group={scale} value="2x" checked/> 2x <input type="radio" bind:group={scale} value="3x"/> 3x <input type="radio" bind:group={scale} value="4x"/> 4x
      </div>
    <br/>
        <input style="display:none" type="file" accept=".jpg, .jpeg, .png" on:change={(e)=>onFileSelected(e)} bind:this={fileinput}>
    <button class="convert" type="button">준비중</button>
</div>
<style>
	#app{
	    display:flex;
		align-items:center;
		justify-content:center;
		flex-flow:column;
    }

    .convert {
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