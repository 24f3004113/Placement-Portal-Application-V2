import { createRouter,createWebHistory } from "vue-router"

import Login from "../views/login.vue"
import StudentRegister from "../views/student_register.vue"
import CompanyRegister from "../views/company_register.vue"

import AdminDashboard from "../views/admin/dashboard.vue"


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
    }

    ]

})

router.afterEach((to) => {
    document.title = to.meta.title || "Placement Portal"
})

export default router