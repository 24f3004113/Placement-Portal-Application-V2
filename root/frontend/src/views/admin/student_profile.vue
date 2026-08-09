<template>

<h2>Student Profile</h2>

<table border="1" v-if="student">

<tbody>

<tr><td>ID</td><td>{{ student.sid }}</td></tr>
<tr><td>Name</td><td>{{ student.name }}</td></tr>
<tr><td>Email</td><td>{{ student.email }}</td></tr>
<tr><td>Phone</td><td>{{ student.phone }}</td></tr>
<tr><td>Course</td><td>{{ student.course }}</td></tr>
<tr><td>CGPA</td><td>{{ student.cgpa }}</td></tr>
<tr><td>Graduation Year</td><td>{{ student.graduation_year }}</td></tr>
<tr><td>Skills</td><td>{{ student.skills }}</td></tr>

</tbody>
</table>

<div v-if="student && student.resume" class="text-center">

<h3>Resume</h3>

<iframe
    :src="'http://127.0.0.1:5000/static/resumes/' + student.resume"
    width="700"
    height="990">
</iframe>

</div>

<p v-else-if="student">Resume not uploaded</p>

<p>{{ message }}</p>

<button @click="$router.back()">Back</button>

</template>

<script>

export default {

data() {
    return {
        student: null,
        message: ""
    }
},

async mounted() {

    let response = await fetch(
        "http://127.0.0.1:5000/admin/student/" +
        this.$route.params.sid,
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
        this.student = data
    else
        this.message = data.message || data.msg
}

}

</script>