import { createRouter,createWebHistory } from "vue-router"

import Login from "../views/login.vue"
import StudentRegister from "../views/student_register.vue"
import CompanyRegister from "../views/company_register.vue"

import AdminDashboard from "../views/admin/dashboard.vue"
import AdminCompanies from "../views/admin/companies.vue"


const router=createRouter({

    history:createWebHistory(),

    routes:[

    {
        path: "/",
        component: Login,
        meta: { title: "Login" }
    },
    {
        path: "/student/register",
        component: StudentRegister,
        meta: { title: "Student Registration" }
    },
    {
        path: "/company/register",
        component: CompanyRegister,
        meta: { title: "Company Registration" }
    },
    {
        path: "/admin",
        component: AdminDashboard,
        meta: { title: "Admin Dashboard" }
    },
    {
        path:"/admin/companies",
        component:AdminCompanies,
        meta:{ title: "Companies" }
    }

    ]

})

router.afterEach((to) => {
    document.title = to.meta.title || "Placement Portal"
})

router.beforeEach((to) => {

    const publicPages = [
        "/",
        "/student/register",
        "/company/register"
    ]

    if (!publicPages.includes(to.path) && !localStorage.getItem("token")) {
        return "/"
    }

})

export default router