<template>

<div class="container mt-4">
    <h2 class="text-center">Student Dashboard</h2>
    <p class="text-center">Welcome {{ student }}</p>

    <div class="text-center mb-3">
        <button class="bg-secondary btn shadow text-white me-2" @click="$router.push('/student/applications')">My Applications</button>
        <button class="bg-secondary btn shadow text-white me-2" @click="$router.push('/student/history')">Application History</button>
        <button class="bg-secondary btn shadow text-white me-2" @click="$router.push('/student/interviews')">My Interviews</button>
        <button class="bg-secondary btn shadow text-white me-2" @click="$router.push('/student/placements')">My Placement</button>
        <button class="bg-secondary btn shadow text-white me-2" @click="$router.push('/student/profile/update')">View/Edit Profile</button>
        <button class="bg-secondary btn shadow text-white" @click="$router.push('/student/resume/update')">View/Update Resume</button>
    </div>

    <div class="row justify-content-center">
        <div class="col-md-8">
            <table class="table table-borderless table-light">
                <thead>
                    <tr>
                        <th class="text-center">Total Applications</th>
                        <th class="text-center">Shortlisted</th>
                        <th class="text-center">Interviews</th>
                        <th class="text-center">Placements</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="text-center">{{ total_applications }}</td>
                        <td class="text-center">{{ shortlisted }}</td>
                        <td class="text-center">{{ interviews }}</td>
                        <td class="text-center">{{ placements }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <h3 class="text-center mt-3">Available Placement Drives</h3>

    <div class="text-center mb-3">
        <input type="text" class="form-control d-inline-block w-50"
            placeholder="Search Company, Job or Description"
            v-model="search" @input="getDashboard">
        <button class="bg-secondary btn shadow text-white ms-2" @click="clearSearch">Clear</button>
    </div>

        <div class="container my-5 shadow p-2 ">
            <div class="table-responsive-md">
                <table class="table table-striped  table-bordered table-hover ">
                <thead>
                    <tr>
                        <th>ID</th><th>Company</th><th>Job Title</th>
                        <th>Salary</th><th>Application Deadline</th><th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="drives.length == 0">
                        <td colspan="6" class="text-center">No placement drives found</td>
                    </tr>
                    <tr v-else v-for="drive in drives" :key="drive.did">
                        <td>{{ drive.did }}</td>
                        <td>{{ drive.company }}</td>
                        <td>{{ drive.job_title }}</td>
                        <td>{{ drive.salary }}</td>
                        <td>{{ drive.application_deadline }}</td>
                        <td>
                            <button class="bg-primary btn shadow text-white me-1"
                                @click="$router.push('/student/drive/' + drive.did)">View Drive Details</button>
                            <button v-if="!drive.applied"
                                class="bg-success btn shadow text-white me-1"
                                @click="apply(drive.did)">Apply</button>
                            <button v-else disabled class="btn btn-warning">Already Applied</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <div class="text-center mt-3">
        <button class="bg-danger btn shadow text-white" @click="logout">Logout</button>
    </div>
</div>

</template>

<script>

export default {

    data() {
        return {
            student: "",
            total_applications: 0,
            shortlisted: 0,
            interviews: 0,
            placements: 0,
            drives: [],
            search: ""
        }
    },

    methods: {

        async getDashboard() {



            let response = await fetch(
                "http://localhost:5000/student/dashboard?search=" + this.search,
                {
                    headers: {
                        "Authorization":
                            "Bearer " + localStorage.getItem("token")
                    },
                    credentials: "include"
                }
            )

            let data = await response.json()

            if ( data.msg == "Token has expired") {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/")
                return
            }

            this.student = data.student
            this.total_applications = data.total_applications
            this.shortlisted = data.shortlisted
            this.interviews = data.interviews
            this.placements = data.placements
            this.drives = data.available_drives
        },

        clearSearch() {
            this.search = ""
            this.getDashboard()
        },

        async apply(did) {

            let response = await fetch(
                "http://localhost:5000/student/drive/" + did + "/apply",
                {
                    method: "POST",
                    headers: {
                        "Authorization":
                            "Bearer " + localStorage.getItem("token")
                    },
                    credentials: "include"
                }
            )

            let data = await response.json()

            alert(data.message)

            if (response.ok)
                this.getDashboard()
        },

        logout() {
            localStorage.removeItem("token")
            this.$router.push("/")
        }

    },

    mounted() {
        this.getDashboard()
    }

}

</script>