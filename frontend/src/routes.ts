// svelte-router documentation https://github.com/jorgegorka/svelte-router
import Home from "./pages/Home.svelte";
import ScanTag from "./pages/parliament/ScanTag.svelte";
import ChooseParty from "./pages/parliament/ChooseParty.svelte";
import ChooseCandidates from "./pages/parliament/ChooseCandidates.svelte";
import ConfirmChoice from "./pages/parliament/ConfirmChoice.svelte";
import SendVote from "./pages/parliament/SendVote.svelte";
import Debug from "./pages/Debug.svelte";
import NotFound404 from "./pages/404.svelte";

const routes = [
    {name: '/', component: Home,},
    {
        name: 'parliament',
        nestedRoutes: [
            {name: 'scan', component: ScanTag},
            {name: 'party', component: ChooseParty},
            {name: 'candidates', component: ChooseCandidates},
            {name: 'confirm', component: ConfirmChoice},
            {name: 'send', component: SendVote}
        ],
    },
    {name: 'debug', component: Debug,},
    // custom 404 route
    {
        name: '404',
        path: '404',
        component: NotFound404
    }
]


export {routes}