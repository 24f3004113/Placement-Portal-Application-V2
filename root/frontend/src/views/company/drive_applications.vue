<template>

    <h1 class="text-center">Drive Applications</h1>

    <h2 class="text-center">Company: {{ company }}</h2>
    <h2 class="text-center">Job Title: {{ drive }}</h2>


    <br>

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
                        <th>Application Date</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>

                <tbody>

                    <tr v-if="applications.length == 0">
                        <td colspan="9">No applications found</td>
                    </tr>

                    <tr v-for="application in applications" :key="application.aid">

                        <td>{{ application.aid }}</td>
                        <td>{{ application.student }}</td>
                        <td>{{ application.email }}</td>
                        <td>{{ application.phone }}</td>
                        <td>{{ application.course }}</td>
                        <td>{{ application.cgpa }}</td>
                        <td>{{ application.application_date }}</td>
                        <td>{{ application.status }}</td>


                        <td>
                            <button class="bg-primary btn shadow text-white me-2"
                                @click="$router.push('/company/application/' + application.aid + '/student')">
                                View Resume
                            </button>

                            <button class="bg-warning btn shadow me-2"
                                @click="$router.push('/company/application/' + application.aid + '/update')">
                                Update
                            </button>

                            <button v-if="application.status == 'Shortlisted'"
                                class="bg-success btn shadow text-white me-2"
                                @click="$router.push('/company/application/' + application.aid + '/interview')">
                                Schedule Interview
                            </button>

                            <button v-if="application.status == 'Interview'" class="bg-info btn shadow"
                                @click="$router.push('/company/application/' + application.aid + '/interview/update')">
                                View / Update Interview
                            </button>


                        </td>

                    </tr>

                </tbody>

            </table>
        </div>
    </div>
    <p>{{ message }}</p>
    <br>
    <div class="text-center mt-3">
        <button class="btn btn-secondary me-2" @click="$router.back()">Back</button>

        <button class="bg-danger btn shadow text-white" @click="$router.push('/logout')">Logout</button>
    </div>



</template>

<script>

export default {

    data() {
        return {
            company: "",
            drive: "",
            applications: [],
            message: ""
        }
    },

    methods: {

        async getApplications() {

            let response = await fetch(
                "http://localhost:5000/company/drive/" +
                this.$route.params.did +
                "/applications",
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
                this.company = data.company
                this.drive = data.drive
                this.applications = data.applications
            } else {
                this.message = data.message
            }

        }

    },

    mounted() {
        this.getApplications()
    }

}

</script>