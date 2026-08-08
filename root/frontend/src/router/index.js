import { createRouter, createWebHistory } from "vue-router"


import Login from "../views/login.vue"
import StudentRegister from "../views/student_register.vue"
import CompanyRegister from "../views/company_register.vue"

import AdminDashboard from "../views/admin/dashboard.vue"
import AdminCompanies from "../views/admin/companies.vue"
import AdminStudents from "../views/admin/students.vue"

import CompanyDashboard from "../views/company/dashboard.vue"
import CreateDrive from "../views/company/create_drive.vue"
import CompanyProfile from "../views/company/profile.vue"
import EditDrive from "../views/company/edit_drive.vue"

import StudentDashboard from "../views/student/dashboard.vue"



const router = createRouter({

    history: createWebHistory(),

    routes: [

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
            path: "/admin/companies",
            component: AdminCompanies,
            meta: { title: "Companies" }
        },
        {
            path: "/admin/students",
            component: AdminStudents,
            meta: { title: "Students" }
        },
        {
            path: "/company",
            component: CompanyDashboard,
            meta: { title: "Company Dashboard" }
        },
        {
            path: "/company/drive/create",
            component: CreateDrive,
            meta: { title: "Create Drive" }
        },
        {
            path: "/company/profile",
            component: CompanyProfile,
            meta: { title: "Company Profile" }
        },
        {
            path: "/company/drive/:did/edit",
            component: EditDrive,
            meta: { title: "Edit Drive" }
        },
        {
            path: "/student",
            component: StudentDashboard,
            meta: { title: "Student Dashboard" }
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