<script lang="ts">
    import PrimaryButton from "../components/buttons/PrimaryButton.svelte";
    import {Navigate} from "svelte-router-spa";
    import MainLayout from "../parts/layouts/MainLayout.svelte";
</script>

<MainLayout>
    <Navigate to="/parliament/scan">
        <PrimaryButton text="[DEV] parlamentné voľby"/>
    </Navigate>
</MainLayout>