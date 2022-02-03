<script lang="ts">
    import {tokenValid} from "../../stores";
    import MainLayout from "../../parts/layouts/MainLayout.svelte";
    import Loader from "../../components/Loader.svelte";
    import {navigateTo} from "svelte-router-spa";

    tokenValid.subscribe(tokenValidValue => {
        if (tokenValidValue) {
            navigateTo('/parliament/party')
        }
    })
</script>

<MainLayout >
    <Loader icon="token" title="Vložte prosím autorizačný token do čítačky" />
</MainLayout>