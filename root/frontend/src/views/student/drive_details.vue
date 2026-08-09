<template>

<h2>Drive Details</h2>

<table border="1" v-if="drive">

<tbody>

<tr>
    <td>Company</td>
    <td>{{ drive.company }}</td>
</tr>

<tr>
    <td>Job Title</td>
    <td>{{ drive.job_title }}</td>
</tr>

<tr>
    <td>Description</td>
    <td>{{ drive.description }}</td>
</tr>

<tr>
    <td>Course</td>
    <td>{{ drive.course }}</td>
</tr>

<tr>
    <td>Minimum CGPA</td>
    <td>{{ drive.min_cgpa }}</td>
</tr>

<tr>
    <td>Graduation Year</td>
    <td>{{ drive.graduation_year }}</td>
</tr>

<tr>
    <td>Salary</td>
    <td>{{ drive.salary }}</td>
</tr>

<tr>
    <td>Application Deadline</td>
    <td>{{ drive.deadline }}</td>
</tr>

</tbody>

</table>

<p>{{ message }}</p>

<button @click="$router.back()">Back</button>

</template>

<script>

export default {

    data() {
        return {
            drive: null,
            message: ""
        }
    },

    async mounted() {

        let response = await fetch(
            "http://127.0.0.1:5000/student/drive/" +
            this.$route.params.did,
            {
                headers: {
                    "Authorization":
                        "Bearer " + localStorage.getItem("token")
                },
                credentials: "include"
            }
        )

        let data = await response.json()

        if (response.status == 401 && data.msg == "Token has expired") {
            alert("Session expired. Please login again.")
            localStorage.removeItem("token")
            this.$router.push("/")
            return
        }

        if (response.ok)
            this.drive = data
        else
            this.message = data.message || data.msg

    }

}

</script>