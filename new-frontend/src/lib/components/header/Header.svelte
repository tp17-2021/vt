<script>
    import {url} from "@roxi/routify";
    import {texts} from "../../../api/stores";

    let title = $texts.elections_name_long.sk;
</script>

<header>
    <div class="header-content">
        <img src={$url("/img/sk.png")} alt="" height="50px"/>
        <div>{title}</div>
    </div>
</header>

<style lang="scss">
    header {
        background-color: black;
        width: 100%;
        overflow: hidden;

        &::after {
			content: "";
			display: block;
			width: 100%;
			height: 3px;
			background-image: -webkit-gradient(linear,left top,right top,from(#fff),color-stop(33.3%,#fff),color-stop(33.3%,#003183),color-stop(66.6%,#003183),color-stop(66.6%,#d0190f),to(#d0190f));
			background-image: -webkit-linear-gradient(left,#fff,#fff 33.3%,#003183 0,#003183 66.6%,#d0190f 0,#d0190f);
			background-image: linear-gradient(90deg,#fff 0,#fff 33.3%,#003183 0,#003183 66.6%,#d0190f 0,#d0190f);
			background-size: 150px 100%;
			background-repeat: repeat;
		}
    }



    .header-content {
        color: white;
        font-size: 24px;

        display: flex;
        place-items: center;
        width: 100%;
        max-width: 768px;

        margin: 1rem auto;

        .header-content > div {
            padding: 0 1rem;
        }
    }

    img {
        margin: 0 1rem;
    }
</style>
