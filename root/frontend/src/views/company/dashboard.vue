<template>

    <h2 class="text-center">{{ company.company_name }} Dashboard</h2>
    <div class="text-center">
        <button class="bg-secondary btn shadow text-white ms-2" @click="$router.push('/company/profile')">Update Profile</button>

        <div class="container mt-4">
            <div class="row justify-content-center">
                <div class="col-md-8">

                    <table class="table table-borderless table-light">
                        <thead>
                            <tr>
                                <th class="text-center">Total Drives</th>
                                <th class="text-center">Total Applications</th>
                                <th class="text-center">Selected Students</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr>
                                <td class="text-center">{{ summary.total_drives }}</td>
                                <td class="text-center">{{ summary.total_applications }}</td>
                                <td class="text-center">{{ summary.selected_students }}</td>
                            </tr>
                        </tbody>
                    </table>

                </div>
            </div>
        </div>
        <hr>
        <br>
        <h2 class="text-center">My Job Drives</h2>
        <div class="text-center">
            <input type="text" placeholder="Search drives" v-model="search" @input="getDashboard">

            <button @click="clearSearch">Clear</button>
        </div>


        <div class="container my-5 shadow p-2 ">
            <div class="table-responsive-md">
                <table class="table table-striped  table-bordered table-hover ">

                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Job Title</th>
                            <th>Course</th>
                            <th>Salary</th>
                            <th>Deadline</th>
                            <th>Approval</th>
                            <th>Status</th>
                            <th>Applications</th>
                            <th>Action</th>
                        </tr>
                    </thead>

                    <tbody>

                        <tr v-if="drives.length == 0">
                            <td colspan="9">No drives found</td>
                        </tr>

                        <tr v-else v-for="drive in drives" :key="drive.did">

                            <td>{{ drive.did }}</td>
                            <td>{{ drive.job_title }}</td>
                            <td>{{ drive.course }}</td>
                            <td>{{ drive.salary }}</td>
                            <td>{{ drive.application_deadline }}</td>
                            <td>{{ drive.approval_status }}</td>
                            <td>{{ drive.status }}</td>
                            <td>{{ drive.applications }}</td>

                            <td>
                                <button class="bg-warning btn shadow me-2"
                                    @click="$router.push('/company/drive/' + drive.did + '/edit')">
                                    Edit
                                </button>

                                <button class="bg-primary btn shadow text-white me-2"
                                    @click="$router.push('/company/drive/' + drive.did + '/applications')">
                                    View Applications
                                </button>

                                <button class="bg-danger btn shadow text-white" @click="deleteDrive(drive.did)">
                                    Delete
                                </button>
                            </td>

                        </tr>

                    </tbody>

                </table>
            </div>
        </div>

        <br>

<button class="bg-success btn shadow text-white me-2"@click="$router.push('/company/drive/create')">Create Drive</button>

<button class="bg-danger btn shadow text-white" @click="logout">Logout</button>
    </div>

</template>


<script>

export default {

    data() {

        return {
            company: {},
            summary: {
                total_drives: 0,
                total_applications: 0,
                selected_students: 0
            },
            drives: [],
            search: ""
        }

    },

    methods: {

        async getDashboard() {

            let response = await fetch(
                "http://localhost:5000/company/dashboard?search=" + this.search,
                {
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    },

                    credentials: "include"
                }
            )

            let data = await response.json()

            if (data.msg == "Token has expired") {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/")
                return
            }

            this.company = data.company
            this.summary = data.summary
            this.drives = data.drives

        },

        clearSearch() {

            this.search = ""
            this.getDashboard()

        },
        async deleteDrive(did) {

            if (!confirm("Do you want to delete this drive?"))
                return

            let response = await fetch(
                "http://localhost:5000/company/drive/" + did,
                {
                    method: "DELETE",
                    headers: {
                        "Authorization":
                            "Bearer " + localStorage.getItem("token")
                    },
                    credentials: "include"
                }
            )

            let data = await response.json()

            if (data.msg == "Token has expired") {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/")
                return
            }

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