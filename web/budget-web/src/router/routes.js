import AddDataView from "../views/AddDataView.vue";
import DashboardView from "../views/DashboardView.vue";
import TableVue from "../views/TableView.vue";
import SettingsView from "../views/SettingsView.vue";

export default [
    { path: "/", redirect: "/dashboard" },
    { path: "/data", component: AddDataView },
    { path: "/dashboard", component: DashboardView },
    { path: "/table", component: TableVue },
    { path: "/settings", component: SettingsView },
];
