<template>

<h2>All Applications</h2>

<input type="text" placeholder="Search" v-model="search" @input="getApplications">
<button @click="clearSearch">Clear</button>

<br><br>

<table border="1">

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

</tr>

</tbody>

</table>

<p>{{ message }}</p>

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
                "http://127.0.0.1:5000/admin/applications?search=" +
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