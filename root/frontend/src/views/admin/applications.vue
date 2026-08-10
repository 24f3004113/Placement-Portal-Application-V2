<template>
    <div class="text-center">
        <h2 class="text-center">All Applications</h2>
        <br>

        <input type="text" placeholder="Search" v-model="search" @input="getApplications">
        <button @click="clearSearch">Clear</button>
    </div>
    <br><br>

    <div class="container my-5 shadow p-2 ">
        <div class="table-responsive-md">
            <table class="table table-striped  table-bordered table-hover ">

                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Student</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Course</th>
                        <th>CGPA</th>
                        <th>Company</th>
                        <th>Job</th>
                        <th>Application Date</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>

                <tbody>

                    <tr v-if="applications.length == 0">
                        <td colspan="10">No applications found</td>
                    </tr>

                    <tr v-for="application in applications" :key="application.aid">

                        <td>{{ application.aid }}</td>
                        <td>{{ application.student }}</td>
                        <td>{{ application.email }}</td>
                        <td>{{ application.phone }}</td>
                        <td>{{ application.course }}</td>
                        <td>{{ application.cgpa }}</td>
                        <td>{{ application.company }}</td>
                        <td>{{ application.job_title }}</td>
                        <td>{{ application.application_date }}</td>
                        <td>{{ application.status }}</td>
                        <td>
                            <button class="bg-primary btn shadow text-white me-2"
                                @click="$router.push('/admin/student/' + application.sid)">
                                View Student
                            </button>

                            <button class="bg-secondary btn shadow text-white"
                                @click="$router.push('/admin/application/' + application.aid + '/history')">
                                History
                            </button>
                        </td>

                    </tr>

                </tbody>

            </table>
        </div>
    </div>



    <div class="text-center mt-3">
        <p>{{ message }}</p>
        <button class="bg-primary btn shadow text-white" @click="$router.push('/admin')">
            Dashboard
        </button>
        <button class="btn btn-secondary me-2" @click="$router.back()">Back</button>
        <button class="bg-danger btn shadow text-white" @click="$router.push('/logout')">Logout</button>
    </div>

</template>

<script>

export default {

    data() {
        return {
            applications: [],
            search: "",
            message: ""
        }
    },

    methods: {

        async getApplications() {

            let response = await fetch(
                "http://localhost:5000/admin/applications?search=" +
                encodeURIComponent(this.search),
                {
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


            if (response.ok) {
                this.applications = data
                this.message = ""
            } else {
                this.message = data.message
            }

        },

        clearSearch() {
            this.search = ""
            this.getApplications()
        }

    },

    mounted() {
        this.getApplications()
    }

}

</script>