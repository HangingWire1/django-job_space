document.addEventListener('DOMContentLoaded', function() {
    function createExperienceRow(value = '') {
        const wrapper = document.createElement('div');
        wrapper.className = 'dynamic-list__item';
        wrapper.innerHTML = `<textarea class="form-control" rows="2" placeholder="e.g. Backend Developer at ACME (2020-2023)">${value}</textarea><button type="button" class="btn btn--danger-outline remove-btn">Remove</button>`;
        wrapper.querySelector('.remove-btn').onclick = () => wrapper.remove();
        return wrapper;
    }

    function createEducationRow(value = '') {
        const wrapper = document.createElement('div');
        wrapper.className = 'dynamic-list__item';
        wrapper.innerHTML = `<textarea class="form-control" rows="2" placeholder="e.g. B.Sc. Computer Science — University X (2015-2019)">${value}</textarea><button type="button" class="btn btn--danger-outline remove-btn">Remove</button>`;
        wrapper.querySelector('.remove-btn').onclick = () => wrapper.remove();
        return wrapper;
    }

    function createSocialRow(key = '', value = '') {
        const wrapper = document.createElement('div');
        wrapper.className = 'dynamic-list__item';
        wrapper.innerHTML = `<div class="key-value-group"><input class="form-control" placeholder="Platform (e.g. LinkedIn)" value="${key}"><input class="form-control" placeholder="URL or handle" value="${value}"></div><button type="button" class="btn btn--danger-outline remove-btn">Remove</button>`;
        wrapper.querySelector('.remove-btn').onclick = () => wrapper.remove();
        return wrapper;
    }

    function createSkillChip(skill) {
        const chip = document.createElement('span');
        chip.className = 'skill-chip';
        chip.textContent = skill;
        chip.title = 'Click to remove';
        chip.onclick = () => chip.remove();
        return chip;
    }

    const employeeForm = document.getElementById('employee-form');
    if (employeeForm) {
        try {
            const expData = JSON.parse(document.getElementById('experience-data').textContent || '[]');
            expData.forEach(x => document.getElementById('experience-list').appendChild(createExperienceRow(x)));
            const eduData = JSON.parse(document.getElementById('education-data').textContent || '[]');
            eduData.forEach(x => document.getElementById('education-list').appendChild(createEducationRow(x)));
            const skillsData = JSON.parse(document.getElementById('skills-data').textContent || '[]');
            skillsData.forEach(s => document.getElementById('skills-list').appendChild(createSkillChip(s)));
            const socialData = JSON.parse(document.getElementById('social-data').textContent || '{}');
            Object.entries(socialData).forEach(([k, v]) => document.getElementById('social-list').appendChild(createSocialRow(k, v)));
        } catch (e) { console.error("Error loading initial form data:", e); }

        document.getElementById('add-experience').addEventListener('click', () => document.getElementById('experience-list').appendChild(createExperienceRow()));
        document.getElementById('add-education').addEventListener('click', () => document.getElementById('education-list').appendChild(createEducationRow()));
        document.getElementById('add-social').addEventListener('click', () => document.getElementById('social-list').appendChild(createSocialRow()));
        document.getElementById('add-skill').addEventListener('click', () => {
            const input = document.getElementById('skill-input');
            const skill = (input.value || '').trim();
            if (skill) {
                document.getElementById('skills-list').appendChild(createSkillChip(skill));
                input.value = '';
                input.focus();
            }
        });
        document.getElementById('skill-input').addEventListener('keydown', (e) => {
            if (e.key === 'Enter') { e.preventDefault(); document.getElementById('add-skill').click(); }
        });

        employeeForm.addEventListener('submit', function() {
            document.querySelector('input[name="experience"]').value = JSON.stringify(Array.from(document.querySelectorAll('#experience-list textarea')).map(n => n.value.trim()).filter(Boolean));
            document.querySelector('input[name="education"]').value = JSON.stringify(Array.from(document.querySelectorAll('#education-list textarea')).map(n => n.value.trim()).filter(Boolean));
            document.querySelector('input[name="skills"]').value = JSON.stringify(Array.from(document.querySelectorAll('#skills-list .skill-chip')).map(c => c.textContent.trim()).filter(Boolean));
            const socialMap = {};
            document.querySelectorAll('#social-list .dynamic-list__item').forEach(row => {
                const inputs = row.querySelectorAll('input');
                const key = inputs[0] ? inputs[0].value.trim() : '';
                const value = inputs[1] ? inputs[1].value.trim() : '';
                if (key) { socialMap[key] = value; }
            });
            document.querySelector('input[name="social_media"]').value = JSON.stringify(socialMap);
        });
    }
});
