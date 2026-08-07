import { createRouter,createWebHistory } from "vue-router"

import Login from "../views/login.vue"
import StudentRegister from "../views/student_register.vue"
import CompanyRegister from "../views/company_register.vue"

import AdminDashboard from "../views/admin/dashboard.vue"


const router=createRouter({

    history:createWebHistory(),

    routes:[

        {
            path:"/",
            component:Login
        },

        {
            path: "/student/register",
            component: StudentRegister
        },

        {
            path:"/company/register",
            component:CompanyRegister
        },

        {
            path:"/admin",
            component:AdminDashboard
        }

    ]

})

export default router