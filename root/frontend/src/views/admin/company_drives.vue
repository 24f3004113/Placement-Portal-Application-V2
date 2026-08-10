<template>

    <h2>Company Drives</h2>

    <p><b>Company:</b> {{ company }}</p>

    <input type="text" placeholder="Search" v-model="search" @input="getDrives">
    <button @click="clearSearch">Clear</button>

    <br><br>

    <div class="container my-5 shadow p-2 ">
        <div class="table-responsive-md">
            <table class="table table-striped  table-bordered table-hover ">

                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Job Title</th>
                        <th>Course</th>
                        <th>Min CGPA</th>
                        <th>Salary</th>
                        <th>Deadline</th>
                        <th>Approval</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>

                <tbody>

                    <tr v-if="drives.length == 0">
                        <td colspan="9">No drives found</td>
                    </tr>

                    <tr v-for="drive in drives" :key="drive.did">

                        <td>{{ drive.did }}</td>
                        <td>{{ drive.job_title }}</td>
                        <td>{{ drive.course }}</td>
                        <td>{{ drive.min_cgpa }}</td>
                        <td>{{ drive.salary }}</td>
                        <td>{{ drive.application_deadline }}</td>
                        <td>{{ drive.approval_status }}</td>
                        <td>{{ drive.status }}</td>

                        <td>
                            <button @click="$router.push('/admin/drive/' + drive.did)">
                                View Details
                            </button>

                            <button @click="$router.push('/admin/drive/' + drive.did + '/applications')">
                                Applications
                            </button>
                        </td>

                    </tr>

                </tbody>

            </table>
        </div>
    </div>

    <br>

    <button @click="$router.back()">Back</button>

    <p>{{ message }}</p>

</template>

<script>

export default {

    data() {
        return {
            company: "",
            drives: [],
            search: "",
            message: ""
        }
    },

    methods: {

        async getDrives() {

            let response = await fetch(
                "http://localhost:5000/admin/company/" +
                this.$route.params.cid +
                "/drives?search=" +
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

            if ( data.msg == "Token has expired") {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/")
                return
            }

            if (response.ok) {
                this.company = data.company
                this.drives = data.drives
                this.message = ""
            } else {
                this.message = data.message
            }

        },

        clearSearch() {
            this.search = ""
            this.getDrives()
        }

    },

    mounted() {
        this.getDrives()
    }

}

</script>