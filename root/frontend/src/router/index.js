import { createRouter,createWebHistory } from "vue-router"

import Login from "../views/login.vue"

import AdminDashboard from "../views/admin/dashboard.vue"


const router=createRouter({

    history:createWebHistory(),

    routes:[

        {
            path:"/",
            component:Login
        },

        {
            path:"/admin",
            component:AdminDashboard
        }

    ]

})

export default router