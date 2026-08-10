import { createRouter, createWebHistory } from "vue-router"


import Login from "../views/login.vue"
import StudentRegister from "../views/student_register.vue"
import CompanyRegister from "../views/company_register.vue"

import AdminDashboard from "../views/admin/dashboard.vue"
import AdminCompanies from "../views/admin/companies.vue"
import AdminCompanyDrives from "../views/admin/company_drives.vue"
import AdminStudents from "../views/admin/students.vue"
import AdminStudentProfile from "../views/admin/student_profile.vue"
import AdminStudentApplications from "../views/admin/student_applications.vue"
import AdminDrives from "../views/admin/drives.vue"
import AdminDriveDetails from "../views/admin/drive_details.vue"
import AdminDriveApplications from "../views/admin/drive_applications.vue"
import AdminApplications from "../views/admin/applications.vue"
import AdminApplicationHistory from "../views/admin/application_history.vue"


import CompanyDashboard from "../views/company/dashboard.vue"
import CreateDrive from "../views/company/create_drive.vue"
import CompanyProfile from "../views/company/profile.vue"
import EditDrive from "../views/company/edit_drive.vue"
import CompanyDriveApplications from "../views/company/drive_applications.vue"
import StudentProfile from "../views/company/student_profile.vue"
import UpdateApplication from "../views/company/update_application.vue"
import ScheduleInterview from "../views/company/schedule_interview.vue"
import UpdateInterview from "../views/company/update_interview.vue"




import StudentDashboard from "../views/student/dashboard.vue"
import UpdateProfile from "../views/student/update_profile.vue"
import UpdateResume from "../views/student/update_resume.vue"
import Applications from "../views/student/applications.vue"
import History from "../views/student/history.vue"
import Interviews from "../views/student/interviews.vue"
import Placements from "../views/student/placements.vue"
import DriveDetails from "../views/student/drive_details.vue"
import ApplicationHistory from "../views/student/application_history.vue"



const router = createRouter({

    history: createWebHistory(),

    routes: [

        {
            path: "/",
            component: Login,
            meta: { title: "Login" }
        },
        {
            path: "/login",
            redirect: "/"
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
            path: "/admin/company/:cid/drives",
            component: AdminCompanyDrives,
            meta: {title: "Company Drives"}
        },
        {
            path: "/admin/students",
            component: AdminStudents,
            meta: { title: "Students" }
        },
        {
            path: "/admin/student/:sid",
            component: AdminStudentProfile
        },
        {
            path: "/admin/student/:sid/applications",
            component: AdminStudentApplications
        },
        {
            path: "/admin/drives",
            component: AdminDrives,
            meta: { title: "Placement Drives" }
        },
        {
            path: "/admin/drive/:did",
            component: AdminDriveDetails
        },
        {
            path: "/admin/drive/:did/applications",
            component: AdminDriveApplications,
            meta: { title: "Drive Applications" }
        },
        {
            path: "/admin/applications",
            component: AdminApplications
        },
        {
            path: "/admin/application/:aid/history",
            component: AdminApplicationHistory
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
            path: "/company/drive/:did/applications",
            component: CompanyDriveApplications,
            meta: { title: "Job Appliactions" }
        },
        {
            path: "/company/application/:aid/student",
            component: StudentProfile
        },
        {
            path: "/company/application/:aid/update",
            component: UpdateApplication,
            meta: { title: "Update Job Appliactions" }
        },
        {
            path: "/company/application/:aid/interview",
            component: ScheduleInterview,
            meta: { title: "Schedule Interview" }
        },
        {
            path: "/company/application/:aid/interview/update",
            component: UpdateInterview,
            meta: { title: "Update Interview" }
        },
        {
            path: "/student",
            component: StudentDashboard,
            meta: { title: "Student Dashboard" }
        },
        {
            path: "/student/profile/update",
            component: UpdateProfile
        },
        {
            path: "/student/resume/update",
            component: UpdateResume
        },
        {
            path: "/student/applications",
            component: Applications
        },
        {
            path: "/student/history",
            component: History
        },
        {
            path: "/student/interviews",
            component: Interviews
        },
        {
            path: "/student/placements",
            component: Placements
        },
        {
            path: "/student/drive/:did",
            component: DriveDetails
        },
        {
            path: "/student/application/:aid/history",
            component: ApplicationHistory
        },
        {
            path: "/logout",
            beforeEnter: (to, from, next) => {
                localStorage.removeItem("token")
                next("/")
            }
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

router.beforeEach((to, from) => {

    if (to.path == "/logout") {
        localStorage.removeItem("token")
        return "/"
    }

    return true
})

export default router