<script>
	import { url } from "@roxi/routify";
	import {texts} from "../../../api/stores";

	let title = $texts.elections_name_long.sk;
</script>

<header>
	<div class="header-content">
		<img src={$url("/img/sk.png")} alt="" height="50px" />
		<div>{title}</div>
	</div>
</header>

<style>
	header {
		background-color: black;
		width: 100%;
	}
	.header-content {
		color: white;
		padding: 1rem;
		font-size: 24px;

		display: flex;
		place-items: center;
		width: 100%;
		max-width: 768px;

		margin: 0 auto;
	}

	img {
		margin-right: 1rem;
		margin-left: 1rem;
	}
</style>
