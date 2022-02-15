<script lang="ts">
    import {config} from "../stores";
</script>

<style>
    header {
        background-color: black;
        color: white;
        width: 100%;
        padding: 1rem;
        font-size: 24px;

        display: flex;
        place-items: center;
    }

    img {
        margin-right: 1rem;
    }
</style>

<header>
    <img src="/img/sk.png" alt="" height="50px">
    <div>{$config.title}</div>
</header>
